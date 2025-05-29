import concurrent.futures
import time
import threading


# 模拟一个I/O密集型任务（如网络请求、文件操作等）
def io_task(task_id, delay=1):
    start = time.perf_counter()
    print(f"▶️ 任务{task_id}启动 | 线程ID：{threading.get_ident()}")
    time.sleep(delay)  # 模拟I/O等待
    end = time.perf_counter()
    print(f"⏹️ 任务{task_id}完成 | 耗时：{end - start:.2f}s")
    return f"任务{task_id}结果"


def main():
    # 任务参数列表（可自定义任务数量和时间）
    tasks = [(i, 1) for i in range(1, 6)]  # 生成5个任务，每个耗时1秒

    # 单线程顺序执行（性能对比）
    print("🚀 单线程执行开始")
    start_single = time.perf_counter()
    results_single = [io_task(*task) for task in tasks]
    print(f"⏱️ 单线程总耗时：{time.perf_counter() - start_single:.2f}s\n")

    # 多线程执行
    print("🚀🚀🚀 多线程执行开始")
    start_multi = time.perf_counter()

    # 使用ThreadPoolExecutor管理线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 提交所有任务到线程池
        futures = [executor.submit(io_task, *task) for task in tasks]

        # 获取任务结果（按完成顺序）
        results_multi = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results_multi.append(result)
            except Exception as e:
                print(f"❌ 任务执行出错：{str(e)}")

    print(f"⏱️ 多线程总耗时：{time.perf_counter() - start_multi:.2f}s")
    print("\n📊 执行结果对比：")
    print(f"单线程结果：{results_single}")
    print(f"多线程结果：{results_multi}")


if __name__ == "__main__":
    main()