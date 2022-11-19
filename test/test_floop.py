from floop.extensions import loop

import pytest


class TestFloop:
    def test_floop(self):

        def counter():
            i = 0
            def _counter():
                nonlocal i
                val = i
                i += 1
                return val
            return _counter

        def fn(counter):
            i = counter()
            if i >= 5:
                return i

        assert loop(fn, counter()) == 5

    def test_raising_exception(self):
        class LoopException(Exception): ...
        def fn():
            raise LoopException("raise exception in loop")
        with pytest.raises(LoopException) as err:
            loop(fn)

        assert err.value.args == ("raise exception in loop",)


    def test_mutable_args(self):

        def fn(coll):
            if coll == []:
                coll.append(1)
            else:
                coll.append(coll[-1]+1)
            if coll[-1] == 5:
                return coll

        assert loop(fn, []) == [1,2,3,4,5]
