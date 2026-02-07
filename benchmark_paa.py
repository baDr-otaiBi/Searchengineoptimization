import time
import people_also_ask
import sys

def benchmark(keyword, limit=5):
    print(f"Benchmarking 'people_also_ask.get_related_questions' for keyword: '{keyword}' with limit: {limit}")
    start_time = time.time()
    try:
        questions = people_also_ask.get_related_questions(keyword, limit)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Success! Found {len(questions)} questions.")
        print(f"Time taken: {duration:.4f} seconds")
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    keyword = "python performance"
    if len(sys.argv) > 1:
        keyword = sys.argv[1]

    benchmark(keyword)
