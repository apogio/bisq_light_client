from datetime import timedelta
import utils.aio
import asyncio 
import sys
import threading
import unittest as _unittest
from bisq.common.setup.common_setup import CommonSetup
from bisq.common.user_thread import UserThread
from utils.twisted_utils import wrap_with_ensure_deferred, twisted_wait, cancel_delayed_calls
from twisted.trial import unittest
class MockExceptionHandler:
    def __init__(self):
        self.exception_caught = False
        
    def handle_uncaught_exception(self, exception, shutdown):
        self.exception_caught = True

class TestExceptionHandler(unittest.TestCase):
    
    def tearDown(self):
        sys.excepthook = sys.__excepthook__
        threading.excepthook = threading.__excepthook__
        cancel_delayed_calls()
    
    @wrap_with_ensure_deferred
    async def test_uncaught_exception_handler_for_user_thread_executed_methods(self):
        mock_handler = MockExceptionHandler()
        CommonSetup.setup_uncaught_exception_handler(mock_handler)

        await twisted_wait(0.5)

        e = asyncio.Event()
        
        def raise_error():
            raise Exception("Test unhandled error")
        
        UserThread.execute(raise_error)
        
        # Wait for the error to be processed
        def check_handler():
            if mock_handler.exception_caught:
                e.set()
        
        # Keep checking until handler catches exception
        check_timer = UserThread.run_periodically(check_handler, timedelta(milliseconds=100))

        try:
            await asyncio.wait_for(e.wait(), 5)
        except asyncio.TimeoutError:
            self.fail("Test timed out waiting for exception handler")
        finally:
            check_timer.stop()
            
        self.assertTrue(mock_handler.exception_caught)
        self.flushLoggedErrors()
        
    @wrap_with_ensure_deferred
    async def test_uncaught_exception_handler_for_threads(self):
        mock_handler = MockExceptionHandler()
        CommonSetup.setup_uncaught_exception_handler(mock_handler)

        def raise_exception():
            raise Exception("Test thread exception")
            
        thread = threading.Thread(target=raise_exception)
        thread.start()
        thread.join()
        
        await twisted_wait(0.5)
        
        self.assertTrue(mock_handler.exception_caught)

if __name__ == '__main__':
    _unittest.main()