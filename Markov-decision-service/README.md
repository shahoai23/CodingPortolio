# Markov Decision Service API

A containerized FastAPI microservice that provides the means to evaluate optimal policies for markov decision processes

## MDP Relative Value Iteration for optimizing average reward

This service enables a user to determine the optimal stationary policy for a problem which can be represented as a markov decision process. It utilizes the relative value iteration approach. It requires square matrices to represent the TPMs and the TRMs. It utilizes a max iteration and max run time as secondary stopping criteria.

## Intended Features

1. Relative value iteration for determining an optimal stationary policy