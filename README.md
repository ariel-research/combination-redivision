# combination-redivision
Fair division of apartments in combination-redivision projects.

Most code was written by Eitan Lichtman.

## Problem description

**Input:**

- $k \in N$ agents, $n \in N$ objects

- Set of object values: $V = \{ v_1, v_2, \ldots ,v_n \} $, $v_i \in \mathbb{N}$

- Set of agents: $A=\{1, \ldots, k\}$

- With corresponding agent rights $\{p_1,\ldots ,p_k\}, p_i\in\mathbb{R^+}$ s.t. $\sum_{j=1}^k p_i=1$.

- The relative-entitlement for agent $i$ is $re_i = sum(V)p_i$.

**Output:**

The algorithm will output an allocation as follows, $\forall$ agent $i$ we will return a group of objects given to agent $i$: $V_i = \{v_{i1}, v_{i2}...v_{im} \}$ for some $m \in \mathbb{N}$.

The balance payment for agent $i$ is calculated as follows: $bp_i=sum(V_i)-re_i$.
Balance payments payed by an agent to the local committee are positive, payments received by an agent from the local committee are negative, if an agent received exactly what he deserves in property his balance payments are 0. $\sum_{j=1}^k bp_i=0$


**Target function:**

The goal is to minimize $\sum_{i=1}^k max(bp_i,0)=\sum_{i=1}^k max(sum(V_i)-re_i,0)$ (the sum of the positive balance payments).

Note that the total of negative balance payments are equal to the total of positive balance payments, and therefore are ignored.

## CGA equal rights

We will present the Complete Greedy Algorithm (CGA) adjusted to combination-redivision. given a group $V$ of $n$ numbers and $k$, let $t$ be the sum of the $V$ and $re = \frac{t}{k}$ the relative entitlement. Our goal is to divide the numbers to $k$ baskets while minimizing the positive balance payments i.e. minimize $\sum_{i=1}^k max(b_i-re,0)$ where $b_i=$ sum of basket $i$.

Like CGA for Min-Dif, CGA for combination-redivision also sorts the numbers in a decreasing order and perform the search in a greedy way (in each iteration we put the next number in the basket with the smallest sum meanwhile). Also, if at any point two partial baskets have the same sum, the next number is only assigned to one of them, to eliminate duplicate nodes.

Now we will explain the differences: CGA for Min-Dif terminates the search when a perfect partition is found with a difference of zero or one because it is definitely optimal. In combination-redivision a result of one is not necessarily optimal. For example, dividing the numbers $\{1,1,1\}$ to $2$ baskets optimally would yield the following division: $\{1,1\},\{1\}$ which gives a result of $0.5$. The question is what is considered a perfect partition in combination-redivision? If $t$ is divisible by $k$, we can get a result of zero. Otherwise, we write $t$ as $t=ak+r$ for some $a,r \in \mathbb{N}$. In the best case scenario (let's say we are dividing $t$ $1's$) we would divide $ak$ equally to the baskets (each basket gets $a$). The remaining $r$ would be divided into $1's$ and we would give 1 to $r$ out of the $k$ baskets. The final result is calculated as follows: $ak$ does not contribute to our result because it is divided equally between the baskets, so it will be ignored. We are left with $r$, giving us a relative entitlement of $re=\frac{r}{k}$. We have $r$ baskets that each contribute $(1-\frac{r}{k})$ to the result, with a total result of $d=r(1-\frac{r}{k})$.

Another difference is that instead of the last rule of CGA, we have the following rule: Let $d$ be the best difference so far. If at any point $\sum_{i=1}^k max(b_i-re,0)\geq d$ terminate the current branch. Meaning, if during the search we already got higher than $d$, continuing to search this branch could just add numbers to baskets and make the result worse than $d$ and not better.

## ILP equal rights

We will present the Integer Linear Programming algorithm adjusted to combination-redivision.
Like ILP for Min-Max we use the following variables: A set of $n$ item values $V = \{ v_1, v_2,\ldots ,v_n \} $, $v_i \in \mathbb{N}$ to divide into $k$ baskets. An indicator variable $I_{ij}$ which is $1$ if integer $v_i$ is assigned to basket $j$ and $0$ otherwise. For the combination-redivision version we add $\forall j \in [1,k]$ the following variables: $z_j = \sum_{j=1}^n(v_i \times I_{ij})-\frac{1}{n}\sum_{j=1}^n(v_i)$ (for each basket, $z_j$ is it's relative entitlement which is the positive or negative distance from the average). We also define the variable $t_j$ that will be $|z_j|$ (we will make sure that it's the absolute value later in the constraints). The Integer programming goes as follows:

![image](https://github.com/ariel-research/combination-redivision/assets/44766460/d1327dbc-d55c-4116-85da-49d6e324a268)

## Black box method

Given an optimal algorithm $A$ for the combination-redivision problem for equal rights (like CGA or ILP), we will show how to use $A$ in order to solve the combination-redivision problem for different rights. Algorithm $A$ receives an input of $n$ numbers and $k$ baskets, and outputs a partition of the numbers into $k$ baskets while minimizing the balance payments.

In order to solve the combination-redivision problem for different rights we use the black box method, meaning we show an algorithm with $A$ being used as a black box. The algorithm works as follows: Given a set $V$ of $n$ numbers and agent rights $\{p_1,\ldots ,p_k\}$, s.t. $\sum_{j=1}^k p_i=1$, execute the following steps:

- Instead of the baskets starting with a sum of $0$, each basket $i$ starts with a sum of: $max(p_1,\ldots ,p_k) (sum(V))-p_i (sum(V))$. We do this in order to convert the problem to a problem with equal rights by matching all of the baskets to the basket with the maximum right.

- Execute $A$ with an input of $V$ and the baskets, receiving an output of the numbers from $V$ allocated into the $k$ baskets.

- Subtract $max\{p_1,\ldots ,p_k\} (sum(V))-p_i (sum(V))$ (the value that we started with) from each basket $i$ and return the final allocation.



[Thesis_Eitan_Lichtman.pdf](https://github.com/user-attachments/files/15904650/Thesis_Eitan_Lichtman.pdf)
