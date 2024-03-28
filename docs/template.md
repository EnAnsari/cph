# Template Description

```cpp
#include<bits/stdc++.h>
```
C++ standard libraries

---
```cpp
#define L(i, j, k) for(int i = (j); i <= (k); ++i)
```
example:
```cpp
#define L(i, j, k) for(int i = (j); i <= (k); ++i)

int main() {
  // Using the macro
  L(x, 1, 5) {
    cout << x << " ";
  }
  cout << endl;
  return 0;
}
```
output:
```
1 2 3 4 5 
```
---
```cpp
#define R(i, j, k) for(int i = (j); i >= (k); --i)
```
example:
```cpp
#define R(i, j, k) for(int i = (j); i >= (k); --i)

int main() {
  // Using the macro
  R(x, 5, 1) {
    cout << x << " ";
  }
  cout << endl;
  return 0;
}
```
output
```
5 4 3 2 1
```
---
```cpp
#define ll long long
```
example:
```cpp
#define ll long long

int main() {
  // Without macro
  long long large_number = 9223372036854775807;  // Maximum value for long long on most systems

  // With macro
  ll large_number = 9223372036854775807;

  cout << "Large number: " << large_number << endl;
  return 0;
}
```
---
```cpp
#define sz(a) ((int) (a).size())
```
example:
```cpp
#include <vector>

#define sz(a) ((int) (a).size())

int main() {
  // Example with a vector
  std::vector<int> my_vector = {1, 2, 3, 4, 5};

  // Using the macro to get the size
  int vector_size = sz(my_vector);

  cout << "Size of the vector: " << vector_size << endl;
  return 0;
}
```
