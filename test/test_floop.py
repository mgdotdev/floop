from floop import loop, config

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


class TestConfig:
    def test_callback(self):
        def fn():
            return 1, 2

        result = loop(config(fn, callback=lambda x, y: x == 1 and y == 2))

        assert result == (1, 2)

    def test_max_iter(self):

        count = 0
        def fn():
            nonlocal count
            count += 1

        loop(config(fn, max_iter=500))

        assert count == 500

    def test_as_decorator_with_kwargs(self):
        count = 0

        @config(max_iter=500)
        def fn():
            nonlocal count
            count += 1

        loop(fn)

        assert count == 500

