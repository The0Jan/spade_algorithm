#### Projekt z przedmiotu :Metody Eksploracji Danych"
Implementacja algorytmu SPADE z artykułu “SPADE: An efficient algorithm for mining frequent sequences” [1].


#### Korzystanie
W ramach wywołania programy na własnym zestawie danych w formacie spmf, wystarczy skorzystać z pliku ‘main.py’, wywołując go jak na przykładzie poniżej:
```
python main.py --data "data/example.txt" --save "results/example.txt" --min_sup 40
```
Argumenty wykorzystywane podczas wywoływania pliku:
•	 ‘--data’ -> ścieżka do pliku z danymi do sekwencji,
•	‘--save’ -> ścieżka gdzie mają zostać zapisane wyniki algorytmu,
•	‘--min_sup’ -> wartość minimalnego wsparcia dla algorytmu SPADE.

Ponadto zostały również udostępnione dwa skrypty i jeden program pythonowy:
•	‘example_test.sh’ -> skrypt służący do wypróbowania działania algorytmu na danych przykładowych zawartych w artykule[1],
•	‘all_data_sequence.sh’ -> skrypt do ponowienia testów wykonanych przy pomocy algorytmu dla różnych zestawów danych i różnych parametrów wsparcia minimalnego (min_sup),
•	‘spmf_sequencing.py’  -> program do wykonania sekwencjonowania przy pomocy biblioteki ‘spmf’[6]  dla wykorzystywanych w analizie zestawów danych i wartości minimalnego wsparcia.

#### Bibliografia
<div id="ref-xie2018" class="csl-entry">
1. Zaki, M. J. ,“SPADE: An efficient algorithm for mining frequent sequences”, Machine learning, vol.42.no.1-2,pp.31-60,2001
</div>
