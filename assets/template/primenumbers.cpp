#include <iostream>
#include <vector>
using namespace std;
int countPrimes(int n) {
  if (n <= 1) {
    return 0;
  }

  // Create a vector to mark prime numbers (initially all True)
  vector<bool> is_prime(n + 1, true);
  is_prime[0] = is_prime[1] = false;  // 0 and 1 are not prime

  // Sieve: Mark multiples of primes as non-prime
  for (int i = 2; i * i <= n; i++) {
    if (is_prime[i]) {
      for (int j = i * i; j <= n; j += i) {
        is_prime[j] = false;
      }
    }
  }

  // Count the primes (excluding 0 and 1)
  int count = 0;
  for (int i = 2; i <= n; i++) {
    if (is_prime[i]) {
      count++;
    }
  }
  return count;
}
int main() {
  int n;
  cout << "Enter the upper limit (n): ";
  cin >> n;

  int prime_count = countPrimes(n);
  cout << "Number of primes less than or equal to " << n << ": " << prime_count << endl;

  return 0;
}
