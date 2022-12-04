const HelpPage = () => {
  return (
    <div className="mt-5">
      <p>Population Size is a subset of solutions in the current generation</p>

      <p>
        Elite schedules: Are the schedules in the current generation with the
        best fitness values. These schedules automatically survive to the next
        generation. The value decides how many make it to the next generation.
      </p>

      <p>
        Mutations rate: This value controls how many random changes, or
        mutations, are introduced to a single parent.
      </p>

      <p>
        Tournament selection size: Tournament selection involves running several
        "tournaments" among a few “Schedules” chosen at random from the
        population. The winner of each tournament (the one with the best
        fitness) is selected for crossover. Since the tournament is based on
        pool size, the larger the tournament size is the likelier weaker
        schedules will be selected, and in turn stronger schedules too.
      </p>

      <p>
        Maximum iteration: The algorithm stops when the number of generations
        reaches MaxIterations
      </p>
    </div>
  );
};

export default HelpPage;
