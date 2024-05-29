#include <iostream>
#include <queue>
using namespace std;

int main() {
	int arr[6] = { 10, 2, 4, 8, 6, 9 };

	priority_queue<int> pq;

	cout << "Array: ";
	for (auto i : arr) {
		cout << i << ' ';
	}
	cout << endl;
	for (int i = 0; i < 6; i++) {
		pq.push(arr[i]);
	}

	cout << "Priority Queue: ";
	while (!pq.empty()) {
		cout << pq.top() << ' ';
		pq.pop();
	}

	return 0;
}
