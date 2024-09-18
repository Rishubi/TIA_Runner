from auto_test import run_test

if __name__ == "__main__":
    compile_passed, num_correct_tests, num_total_tests, message = run_test(problem_id='GetBitStates', problem_dir='cases') # problem_dir最好为绝对路径
    if compile_passed:
        print(f"过编译，通过测例{num_correct_tests}，总测例{num_total_tests}")
    else:
        print(f"未过编译，报错：\n{message}")
