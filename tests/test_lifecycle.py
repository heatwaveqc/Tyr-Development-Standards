import pathlib
import os
import unittest
from unittest.mock import patch
import types

ROOT = pathlib.Path(__file__).resolve().parents[1]
def load():
    raw = (ROOT / ".github/workflows/lifecycle-audit.yml").read_text()
    source = raw.split("<<'TYR_PYTHON'\n", 1)[1].split("\n          TYR_PYTHON", 1)[0]
    mod = types.ModuleType("lifecycle")
    exec(compile("\n".join(line[10:] for line in source.splitlines()), "embedded-audit", "exec"), mod.__dict__)
    mod.REPO = "example/project"
    return mod

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
    def test_budget(self):
        with patch.dict(os.environ, {"BRANCH_BUDGET":"12"}):
            self.assertEqual([self.m.branch_budget(n) for n in (12,13,22,23)], ["HEALTHY","REVIEW","REVIEW","MAINTENANCE"])
    def test_refs(self):
        p = {"head":{"ref":"fork","repo":{"full_name":"other/fork"}},"base":{"ref":"main","repo":{"full_name":"example/project"}}}
        self.assertEqual(self.m.local_pr_refs([p]), {"main"})
    def test_pagination(self):
        with patch.object(self.m,"api",side_effect=[list(range(100)),[100]]) as api:
            self.assertEqual(self.m.pages("/branches"),list(range(101)))
            self.assertEqual(api.call_count,2)
    def test_rename_overlap_and_cross_base(self):
        prs = [{"number":1,"base":{"ref":"main"}},{"number":2,"base":{"ref":"main"}},{"number":3,"base":{"ref":"other"}}]
        data = {"/pulls?state=open":prs,"/pulls/1/files":[{"filename":"new","previous_filename":"old"}],"/pulls/2/files":[{"filename":"old"}]}
        with patch.object(self.m,"pages",side_effect=data.__getitem__),patch.object(self.m,"report") as report:
            self.m.collision(1)
            self.assertIn("PR #2: 1 path(s): old"," ".join(report.call_args.args[0]))
    def test_cap(self):
        prs = [{"number":1,"base":{"ref":"main"}}]
        with patch.object(self.m,"pages",side_effect=[prs,[{"filename":"x"}]*3000]):
            with self.assertRaises(ValueError):
                self.m.collision(1)
    def test_inventory_default_and_donors(self):
        sha = "a"*40
        with patch.dict(os.environ,{"PROTECTED_DONORS":"feature/donor","PERMANENT_BRANCHES":"dev","BRANCH_BUDGET":"20"}),patch.object(self.m,"api",side_effect=lambda p: {"default_branch":"trunk"} if p=="" else {"commit":{"committer":{"date":"2020-01-01T00:00:00Z"}}}),patch.object(self.m,"pages",side_effect=[[{"name":"trunk","commit":{"sha":sha}},{"name":"feature/donor","commit":{"sha":sha}}],[],[]]),patch.object(self.m,"report") as report:
            self.m.inventory()
            output=" ".join(report.call_args.args[0])
            self.assertIn("trunk | aaaaaaaaaaaa | permanent/protected",output)
            self.assertIn("external donor; retain",output)
    def test_read_only(self):
        with patch.dict(os.environ,{"GITHUB_TOKEN":"fake"}),patch.object(self.m.urllib.request,"urlopen") as open_url,patch.object(self.m.json,"load",return_value={}):
            self.m.api("/branches")
            self.assertEqual(open_url.call_args.args[0].get_method(),"GET")

if __name__ == "__main__":
    unittest.main()
