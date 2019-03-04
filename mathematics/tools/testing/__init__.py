def name_func(arg):
    return getattr(arg, "__qualname__", str(arg))


# def custom_name_func(testcase_func, param_num, param):
#     def string_summary(s, start, tail):
#         return s[:start] + "﹍" + s[-tail:] if len(s) > start + tail else s
#
#     from parameterized import parameterized
#
#     return "︳".join(
#         [
#             x
#             for x in [
#                 f"{parameterized.to_safe_name(getattr(testcase_func,'__name__',testcase_func.__name__))}-{param_num}",
#                 "︳".join(
#                     [
#                         f"{arg_no}º︴{string_summary(parameterized.to_safe_name(getattr(arg,'__qualname__',str(arg))), 30, 10)}︴"
#                         for arg_no, arg in enumerate(param.args)
#                     ]
#                 ),
#             ]
#         ]
#     )
