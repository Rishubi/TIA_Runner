# Parse compile result
def check_compile_pass(message, problem_id=None):
    last_line = message.strip().split('\n')[-1]
    if '存在错误。' in last_line or '.scl 成功' not in last_line:
        return False
    if problem_id and f'正在生成块 "{problem_id}"' not in message:
        return False
    return True

# Parse test result
def check_test_result(message):
    lines = message.strip().split('\n')
    if '存在错误。' in lines[-1] or '不满足执行' in lines[-1]:
        return False, 0, 100
    num_correct, num_total = 0, 0
    for l in lines:
        bs = l.split(',', 2)
        if len(bs) >= 2:
            if bs[1] == '通过':
                num_correct += 1
                num_total += 1
            elif bs[1] == '失败':
                num_total += 1
    return True, num_correct, num_total
