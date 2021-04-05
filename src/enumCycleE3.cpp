#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <omp.h>
#include <sstream>
#include <string>
#include <vector>

#define UPPER_RATIO 4

std::vector<std::vector<int>>
readGraph(const std::string graph_name)
{
  std::ifstream infile("./input_graphs/" + graph_name + ".in");
  if (infile.fail()) {
    throw std::invalid_argument("Corresponding graph input is not found.\n");
  }

  std::vector<std::vector<int>> graph_v;

  std::string line;
  while (std::getline(infile, line)) {
    std::vector<int> row;
    std::stringstream ss(line);

    int temp;
    while (ss >> temp) {
      row.push_back(temp);
    }
    graph_v.push_back(row);
  }
  return graph_v;
}

void
backtrack(std::vector<int> curr_path,
          const int curr_v,
          const std::vector<std::vector<int>>& graph_v)
{
  curr_path.push_back(curr_v);

  for (auto neig : graph_v[curr_v]) {
    if (neig == curr_path.front()) {
      std::stringstream buff;
      for (auto i : curr_path) {
        buff << i + 1 << ' ';
      }
      buff << "\n";
#pragma omp critical
      std::cout << buff.rdbuf();
    } else if (!(std::find(curr_path.begin(), curr_path.end(), neig) !=
                 curr_path.end()) &&
               (neig > curr_path.front())) {
      if (neig > graph_v.size() / UPPER_RATIO) {
        backtrack(curr_path, neig, graph_v);
      } else {
#pragma omp task
        {
          backtrack(curr_path, neig, graph_v);
        }
      }
    }
  }
}

int
main(int argc, char* argv[])
{
  std::ios::sync_with_stdio(false);
  if (argc != 2) {
    throw std::invalid_argument("Invalid number of arguments!\n");
  }
  std::string graph_name(argv[1]);

  std::ofstream out("./results/" + graph_name + "_E3.out");
  std::streambuf* coutbuf = std::cout.rdbuf(); // save old buf
  std::cout.rdbuf(out.rdbuf());                // redirect std::cout to .out!

  std::vector<std::vector<int>> graph_v = readGraph(graph_name);

  printf("Graph is read.");
  printf("\n|V|= %d\n", graph_v.size());

  for (int i = 0; i < graph_v.size(); i++) {
    printf("%d: ", i + 1);
    for (auto el : graph_v[i]) {
      printf("%d, ", el + 1);
    }
    printf(";\n");
  }

  printf("--->\n");
  printf("Cycles will be enumerated to the file: ./results/%s_E3.out for %s.",
         argv[1],
         argv[1]);

  std::chrono::steady_clock::time_point begin =
    std::chrono::steady_clock::now();

  std::string n_threads;
#pragma omp parallel
  {
#pragma omp for schedule(dynamic)
    for (int i = 0; i < graph_v.size(); i++) {
      std::vector<int> path_init;
      backtrack(path_init, i, graph_v);
    }
    n_threads = std::to_string(omp_get_max_threads());
  }
  std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

  float elapsed_time =
    std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count();
  printf("\nElapsed time is %f ms\n", elapsed_time); // or microseconds µs

  printf("\nNumber of threads: %s\n", n_threads.c_str());

  std::ofstream out_time;
  out_time.open("./results/time_results/" + graph_name + "_thd" + n_threads +
                  "_time_E3.txt",
                std::ios_base::app);
  out_time << elapsed_time << "\n";

  printf("\nDone!");
}
