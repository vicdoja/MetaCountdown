![MetaCountdown's logo](./docs/twitter_header_photo_1.png)
[![license](https://img.shields.io/github/license/vicdoja/MetaCountdown)](https://github.com/vicdoja/MetaCountdown/blob/main/LICENSE)

# MetaCountdown
> A complex problem made simple!

The aim of this package is to find good (ideally optimal) solutions to problem of the number's round of "Countdown" ([1]). This problem involves a list of 6 numbers and an objective number. The objective is to find a mathematical expression using simple operators (addition, substraction, multiplication and division) whose evaluation is the closest to the objective number. Not all numbers in the list have to be used in the expression and a number can be repeated at most the number of times it appears in the list.

In general, what we are looking for is to find a binary tree ([7]) (where terminal nodes are numbers and non-terminal nodes are operators) such that its evaluation is the closest possible to the objective number.

In order to achieve this, we use two different metaheuristics (hence the name of the package). The two metaheristics are genetic algorithms ([2]) and simulated annealing ([3]). For the genetic algorithms, the package called DEAP (Distributed Evolutionary Algorithms in Python) ([4]) is used, and for simulated annealing the package simanneal ([5]) is used. 

Here we use external packages just to make the initial development much simpler, but it's possible that in the future the package is extended so that it uses its own code for metaheuristics.

## Origin

The origin of this project is a subject of the Master's I'm enrolled in. There we were required to use two different metaheuristics to optimize solutions of a complex problem of choice.

After seeing that I could implement and spin the code into a package, I did it without a doubt.

Thanks to developing this project I now have a much wider understanding of Python packages and project management.

## Contributing

This project is currently being developed only by me (Víctor Dorado), but if anyone is interested in contributing to the project, feel free to open some issues, fork the repository and make pull requests or contact me. Every bit of help is welcome!

## References

(1) https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_round

(2) https://en.wikipedia.org/wiki/Genetic_algorithm

(3) https://en.wikipedia.org/wiki/Simulated_annealing

(4) https://github.com/DEAP/deap

(5) https://github.com/perrygeo/simanneal

(6) https://en.wikipedia.org/wiki/Reverse_Polish_notation

(7) https://en.wikipedia.org/wiki/Tree_(data_structure)



[1]: https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_round

[2]: https://en.wikipedia.org/wiki/Genetic_algorithm

[3]: https://en.wikipedia.org/wiki/Simulated_annealing

[4]: https://github.com/DEAP/deap

[5]: https://github.com/perrygeo/simanneal

[6]: https://en.wikipedia.org/wiki/Reverse_Polish_notation

[7]: https://en.wikipedia.org/wiki/Tree_(data_structure)

## Contact

You can open issues and submit pull requests, but if someone wants to talk to me, I'm reachable via my email: thevidoja@gmail.com.

And if someone wants to learn more about me, I have a nice [online version of my CV](https://vicdoja.github.io/), where anyone can find additional information about me and other projects I worked on (this is the only one I can show right now).

## License

This project is licensed under the version 3 of the GNU General Public License. More about it in the [LICENSE file](https://github.com/vicdoja/MetaCountdown/blob/main/LICENSE).
