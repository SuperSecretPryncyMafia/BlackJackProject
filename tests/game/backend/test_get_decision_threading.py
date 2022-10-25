import unittest
import threading
import time


class TestGetDecision(unittest.TestCase):
    def setUp(self):
        self.test_obj = TestObjectWithAtribute()

    def test_if_stops(self):
        result = self.test_obj.start_test()
        self.assertEqual(result, 0)


class TestObjectWithAtribute:
    count = 0
    stop = False

    def __init__(self):
        self.stopping_thread = threading.Thread(target=self.stopping_function, args=[])

    def start_test(self):
        self.stopping_thread.start()
        result = self.loop_function()
        self.stopping_thread.join()
        return result

    def stopping_function(self):
        while True:
            if self.count >= 3:
                self.count = 0
                self.stop = True
                break

    def loop_function(self):
        while self.count < 5:
            if self.stop:
                print("Injecting Virus")
                print("He is SO BIG!\nHEEeeEEe@#ell ^ll l p #%^.   . $%^ ^&*()    .")
                break
            time.sleep(0.25)
            self.count += 1
            print(self.count)
        return 0
