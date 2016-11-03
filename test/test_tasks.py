import unittest
import logging
import yaml
from pprint import pprint, pformat
from skopt import tasks
from subprocess import CalledProcessError


class TasksCreationTest(unittest.TestCase):
    """Check if we can create and execute tasks."""

    def test_passtask(self):
        """Can we declare and execute a task successfully"""
        t1 = tasks.RunTask(exe='python', wd='testtasks', inp='pass.py')
        self.assertListEqual(t1.cmd,['python', 'pass.py'])
        self.assertEqual(t1.wd, 'testtasks')
        self.assertTrue(isinstance(t1.logger,logging.Logger))
        t1()
        self.assertEqual(t1.out, "Running to pass!\n")

    def test_passtask_listcmd_listinp(self):
        """Can we declare tasks with multiple input arguments?"""
        t1 = tasks.RunTask(exe=['python', 'pass.py'])
        self.assertListEqual(t1.cmd,['python', 'pass.py'])
        t2 = tasks.RunTask(exe=['python', 'pass.py'], inp=['monkey','boogie'])
        self.assertListEqual(t2.cmd,['python', 'pass.py', 'monkey', 'boogie'])

    def test_task_fail(self):
        """Can we fail a task due to non-zero return status of executable?"""
        t1 = tasks.RunTask(exe='python', wd='testtasks', inp='fail.py')
        self.assertRaises(CalledProcessError, t1)
        self.assertEqual(t1.out, "About to fail...\n")


class TasksParsingTest(unittest.TestCase):
    """Check if we can create and execute tasks."""

    yamldata="""
        tasks:
            #- set: [parfile, workdir, optional_arguments]
            #- run: [exe, workdir, arguments] 
            #- get: [what, source, destination, optional_arguments]
            - set: [current.par, skf, ]
            - run: [skgen, skf, ]
            - run: [bs_dftb, Si, ]
            - run: [bs_dftb, SiO2, ]
            - get: [get_dftb, Si, Si]
            - get: [get_dftb, SiO2, SiO2]
            - get: [get_meff, Si/bs, Si/bs]
        """
    taskmapper = {'run': tasks.RunTask, 'set': tasks.SetTask, 'get': tasks.GetTask}

    def test_parsetask(self):
        """Can we parse task declarations successfully"""
        spec = yaml.load(self.yamldata)['tasks']
        tasklist = []
        for tt in spec:
            # we should be getting 1 dict entry only!
            (_t, _args), = tt.items()
            try:
                a0 = _args.pop(0)
                a1 = _args.pop(0)
                tasklist.append(self.taskmapper[_t](a0, a1, *_args))
            except TypeError:
                # end up here if unknown task type, which is mapped to None
                self.assertEqual(self.taskmapper.get(_t, None), None)
                pass
        self.assertTrue(isinstance(tasklist[0], tasks.SetTask))
        cmd = ['skgen', 'bs_dftb', 'bs_dftb']
        wd  = ['skf', 'Si', 'SiO2']
        for ii, tt in enumerate(tasklist[1:4]):
            self.assertTrue(isinstance(tt, tasks.RunTask))
            self.assertListEqual(tt.cmd, [cmd[ii]])
            self.assertEqual(tt.wd, wd[ii])
        fun = ['get_dftb', 'get_dftb', 'get_meff']
        src = ['Si', 'SiO2', 'Si/bs']
        for ii, tt in enumerate(tasklist[4:]):
            self.assertTrue(isinstance(tt, tasks.GetTask))
            self.assertEqual(tt.src, src[ii])
            self.assertEqual(tt.dst, src[ii])


class GetTaskTest(unittest.TestCase):
    """Does GetTask operate correctly?"""

    def func_1(self, src, dst, *args, **kwargs):
        assert(isinstance(src, dict))
        assert(isinstance(dst, dict))
        assert('key' in src)
        dst['key'] = src['key']
        
    def func_2(self, src, dst, *args, **kwargs):
        assert(isinstance(src,dict))
        assert(isinstance(dst,dict))
        key = args[0]
        dst[key] = src[key] 

    def func_3(self, src, dst, *args, **kwargs):
        assert(isinstance(src,dict))
        assert(isinstance(dst,dict))
        key = kwargs['query']
        assert key=='key'
        dst[key] = src[key] 

    def test_gettasks_noargs(self):
        """Can we declare and execute a GetTask?"""
        src = {}
        dst = {}
        # declare: pass empty dictionaries
        tt = tasks.GetTask(self.func_1, src, dst)
        self.assertEqual(tt.func, self.func_1)
        self.assertEqual(tt.src, src)
        self.assertEqual(tt.dst, dst)
        # update source dictionary
        src['key'] = True
        src['other'] = False
        # call
        tt()
        # check destination
        self.assertTrue(dst['key'])

    def test_gettasks_posargs(self):
        """Can we declare a GetTask with positional args and execute it?"""
        src = {}
        dst = {}
        # declare: pass empty dictionaries
        tt = tasks.GetTask(self.func_2, src, dst, 'key')
        self.assertEqual(tt.func, self.func_2)
        self.assertEqual(tt.src, src)
        self.assertEqual(tt.dst, dst)
        # update source dictionary
        src['key'] = True
        src['other'] = False
        # call
        tt()
        # check destination
        self.assertTrue(dst['key'])

    def test_gettasks_kwargs(self):
        """Can we declare a GetTask with keyword args and execute it?"""
        src = {}
        dst = {}
        # declare: pass empty dictionaries
        tt = tasks.GetTask(self.func_3, src, dst, query='key')
        self.assertEqual(tt.func, self.func_3)
        self.assertEqual(tt.src, src)
        self.assertEqual(tt.dst, dst)
        # update source dictionary
        src['key'] = True
        src['other'] = False
        # call
        tt()
        # check destination
        self.assertTrue(dst['key'])

if __name__ == '__main__':
    unittest.main()


