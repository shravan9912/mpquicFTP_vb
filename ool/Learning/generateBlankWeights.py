from agentModel import generate_agent


def main():
    # First, generate a blank NN for the agent
    dqn_agent = generate_agent()
    # Next, save NN into h5f file to be loaded by online multipath scheduler
    dqn_agent.save_weights("./blank_weights.h5f", overwrite=True)


if __name__ == "__main__":
    main()
