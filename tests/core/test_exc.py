from cement.core.exc import CaughtSignal, FrameworkError, InterfaceError

from pytest import raises


class TestExceptions:
    def test_frameworkerror(self):
        with raises(FrameworkError, match=".*framework exception.*"):
            raise FrameworkError("test framework exception message")

    def test_interfaceerror(self):
        with raises(InterfaceError, match=".*interface exception.*"):
            raise InterfaceError("test interface exception message")

    def test_caughtsignal(self):
        with raises(CaughtSignal, match=".*Caught signal.*") as e:
            raise CaughtSignal(1, 2)
        assert e.value.signum == 1
        assert e.value.frame == 2
