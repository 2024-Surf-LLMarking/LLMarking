import unittest
from utils.dynamic_utils import (
    extract_info,
    build_diction_from_model,
    build_diction_from_teacher,
)


class TestDynamicUtils(unittest.TestCase):
    def test_extract_info(self):
        test_data = {
            "question1": {
                "teacherMark": "<Point1:True><Point2:False><Point3:True>",
                "feedback_1": "<Point1:True> *True* (Good)\n\n<Point2:False> *False* (Missing)\n\n<Point3:True> *True* (Excellent)",
                "feedback_2": "<Point1:True> *True* (Great)\n\n<Point2:True> *True* (Improved)\n\n<Point3:False> *False* (Needs work)",
                "feedback_3": "<Point1:False> *False* (Incorrect)\n\n<Point2:True> *True* (Good job)\n\n<Point3:True> *True* (Perfect)",
            },
            "question2": {
                "teacherMark": "<Point1:False><Point2:True><Point3:False>",
                "feedback_1": "<Point1:False> *False* (Incorrect)\n\n<Point2:True> *True* (Good)\n\n<Point3:False> *False* (Missing)",
                "feedback_2": "<Point1:True> *True* (Improved)\n\n<Point2:True> *True* (Excellent)\n\n<Point3:False> *False* (Still missing)",
                "feedback_3": "<Point1:False> *xxx* (Wrong)\n\n<Point2:True> *True* (Correct)\n\n<Point3:True> *True* (Added)",
            },
            "question3": {
                "teacherMark": "<Point1:True><Point2:True><Point3:True>",
                "feedback_1": "<Point1:True> *True* (Perfect)\n\n<Point2:True> *True* (Excellent)\n\n<Point3:True> *True* (Great)",
                "feedback_2": "<Point1:True> *xxx* (Good)\n\n<Point2:False> *False* (Missed this)\n\n<Point3:True> *True* (Well done)",
                "feedback_3": "<Point1:True> *xxx* (Correct)\n\n<Point2:True> *True* (Nice)\n\n<Point3:False> *False* (Overlooked)",
            },
        }
        model_marklist, teacher_marklist, mismatch_percentage = extract_info(test_data)

        self.assertEqual(len(model_marklist), 3)
        self.assertEqual(len(teacher_marklist), 3)
        self.assertEqual(
            model_marklist[0], {"Point1": "True", "Point2": "True", "Point3": "True"}
        )
        self.assertEqual(
            teacher_marklist[0], {"Point1": "True", "Point2": "False", "Point3": "True"}
        )
        self.assertEqual(
            model_marklist[1], {"Point1": "True", "Point2": "True", "Point3": "False"}
        )
        self.assertEqual(
            teacher_marklist[1],
            {"Point1": "False", "Point2": "True", "Point3": "False"},
        )
        self.assertEqual(
            model_marklist[2], {"Point1": "False", "Point2": "True", "Point3": "True"}
        )
        self.assertEqual(
            teacher_marklist[2], {"Point1": "True", "Point2": "True", "Point3": "True"}
        )
        # self.assertAlmostEqual(mismatch_percentage, 0, places=2)

    def test_build_diction_from_model(self):
        feedbacks = [
            "<Point1:True> *True* (Good)\n\n<Point2:False> *False* (Missing)",
            "<Point1:True> *True* (Great)\n\n<Point2:True> *True* (Improved)",
            "<Point1:False> *False* (Incorrect)\n\n<Point2:True> *True* (Good job)",
        ]
        teacher_mark = {"Point1": "True", "Point2": "False"}

        result, mismatch_count = build_diction_from_model(
            feedbacks, len(teacher_mark), teacher_mark
        )

        self.assertEqual(result, {"Point1": "True", "Point2": "True"})
        # self.assertEqual(mismatch_count, 0)

    def test_build_diction_from_teacher(self):
        input_str = "<Point1:True><Point2:False><Point3:True>"
        result = build_diction_from_teacher(input_str)

        self.assertEqual(
            result, {"Point1": "True", "Point2": "False", "Point3": "True"}
        )


if __name__ == "__main__":
    unittest.main()
