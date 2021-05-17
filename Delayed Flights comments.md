## Tasca 5. Exploració de les dades

- [Exercici 1](#Exercici1)  
    - [x] Descarrega el data set Airlines Delay: Airline on-time statistics and delay causes i carrega’l a un pandas Dataframe.   
    - [ ] Explora les dades que conté, i queda’t únicament amb les columnes que consideris rellevants.

    - [ ] Busquem fonts addicionals de dades pels aeroports:
        - [Aeroports](http://stat-computing.org/dataexpo/2009/airports.csv)
        - També descarreguem de [https://openflights.org/data.html](https://openflights.org/data.html) el *airports.dat* que conté les zones horàries dels aeroports

- [Exercici 2](#Exercici2)  
  Fes un informe complet del data set:.
  Resumeix estadísticament les columnes d’interès
    - [x] Troba quantes dades faltants hi ha per columna
    - [ ] Crea columnes noves (velocitat mitjana del vol, si ha arribat tard o no...)
    - [ ] Taula de les aerolínies amb més endarreriments acumulats
    - [ ] Quins són els vols més llargs? I els més endarrerits?
    - [ ] Etc.


- [Exercici 3](#Exercici3)  
    - [x] Exporta el data set net i amb les noves columnes a Excel.
        - [ ] Dataset Net: *CleanDelayedFlights.pickle* Es el que utilitzarem a l'algoritmia
        - [ ] Dataset Agregats: *AggDelayedFlights.pickle* L'usarem en algun exercici de visualització


# Netejar el Dataset

## Dataset: Delayed_Flights

### Camps:

|Camp|Escollit|Tipus|Descripció|
|-|:-:|:-|-|
|Year|N|int64|Any|
|Month|N|int64|Mes|
|DayofMonth|N|int64|Dia|
|DayOfWeek|N|int64|Dia de la setmana|
|DepTime|N|float64|**Hora de Sortida**. Guardat amb un decimal al csv<br>El convertirem en camp hora<br>El convertirem en datetime|
|CRSDepTime|N|int64|Computerized Reservations Systems Departure Time. <br>Hora teòrica de sortida (local time:**hhmm**)<br>El convertirem en datetime|
|ArrTime|Y|float64|**Hora d'arribada**<br>El recalcularem|
|CRSArrTime|Y|int64|CRS Arrival Time (local time:**hhmm**)|
|UniqueCarrier|Y|object|Codi de la companyia|
|FlightNum|N|int64|Número de Vol|
|TailNum|N|object|Número de cua. Número de l'avió|
|ActualElapsedTime|Y|float64|Temps en minuts. Es una suma de *AirTime, TaxiIn* i *TaxiOut*|
|CRSElapsedTime|Y|float64|CRS Elapsed Time of Flight, en minuts. Minuts teòrics de duració de vol|
|AirTime|N|float64| Temps de vol|
|ArrDelay|Y|float64| Diferència en minuts entre planificat i real en els vols a la sortida.<br>Quan negatiu ha arribat abans|
|DepDelay|Y|float64| Diferència en minuts entre planificat i real en els vols a l'arribada|
|Origin|Y|object| Aeroport d'Origen|
|Dest|Y|object| Aeropoort d'Arribada|
|Distance|Y|int64| Distància entre aeroports (en milles)|
|TaxiIn|N|float64| Taxi in Time, en minuts|
|TaxiOut|N|float64| Taxi Out Time, en minuts|
|||**Calcel·lacions**|
|Cancelled|Y|int64| Indicador de vol cancel·lat (1=cancel·lat)|
|CancellationCode|N|object| Raons de la cancel·lació<br>- A Carrier<br>- B Weather<br>- C National Air System <br>- D Security|
|Diverted|Y|int64| Indicador de vol desviat (1=Desviat)|
|||**Causes de retràs**|
|CarrierDelay|N|float64|Retràs causat per la companyia, en minuts|
|WeatherDelay|N|float64|Retràs causat pel temps|
|NASDelay|N|float64|Retràs causat per Sistema Aeri(NAS)|
|SecurityDelay|N|float64|Retràs causat per seguretat|
|LateAircraftDelay|N|float64|Retràs causat per arribada retrasada de l'avió|



### Nous camps 

|Camp|Type|Descripció|
|-|-|-|
|carrier_name|object|Nom de la companyia aèria|
|DepartureTime|datetime|Hora de sortida real|
|CRSDepartureTime|datetime|Hora de sortida programada|
|ArrivalTime|datetime|Hora d'arribada real *suma de DepartureTime i ActualElapsedTime*<br>Hauria de coincidir amb ArrTime|
|CRSArrivalTime|datetime|Hora d'arribada programada *suma de CRSDepartureTime i CRSElapsedTime*<br>Hauria de coincidir amb CRSArrTime|
|dia_add||Indica que el DepTime era 2400|
|CRSdia_add||Indica que el DepTime era 2400|
|no_vol|||
|ActualElapsedTime_c|||
|CRSElapsedTime_c||CRSElapsedTime pero amb els outliers modificats a la mitjana|
|endarrerit|||
|||**Aeroports**|
|Name_Origin|object|Nom de l'aeroport d'Origen|
|Name_Dest|object|Nom de l'aeroport de Destí|
|Dep_dailyf||Número de vols que surten aquest dia a l'aeroport Origin|
|Arr_dailyf||Número de vols que arriben aquest dia a l'aeroport Dest|
|||**Companyies**|
|carrier_name|object|Nom de la companyia|
||||



> Considerar buscar el Timezone dels aeroports per a poder ajustar les hores d'arribada

## Pasos

- [ ] First Analysis  
- [ ] Clean Data  
- [ ] Second Analysis  
- [ ] Feature Engineering  


### Comentaris
Timezones dels aeroports... afecta als Delays? Afecta als CRSElapsedTime?

CRSElapsedTime


$$
\begin{equation}
  \left\{
    \begin{alignedat}{2}
      u_0 &=p_0 \\ 
      u_1 &=p_0+p_1&&=u_0+p_1  \\
      u_2 &=p_0+p_1+p_2&&=u_1+p_2  \\
      \vdots \\
      u_{n-1} &=p_0+p_1+\dots + p_{n-1} &&= u_{n-2}+p_{n-1}  \\
      u_{n} &=p_0+p_1+\dots + p_{n} &&= u_{n-1}+p_{n}  \\
    \end{alignedat}
  \right.
\end{equation}
$$

$$
\begin{align}
&\mathbf{\text{Algorithm 1: DDPG algorithm }}\\
&\hline\\
&\text{Randomly initialize critic network $Q(s,a|\theta^Q)$ and actor $\mu(s|\theta^\mu)$ with weights $\theta^Q$ and $\theta^\mu$.}\\
& \text{Initialize target network $Q'$ and $\mu'$ with weights $\theta^{Q'} \leftarrow \theta^Q, \theta^{\mu'} \leftarrow \theta^\mu$ .}\\
&\text{Initialize replay buffer $R$}\\
&\mathbf{ \text{for}} \text{ episode = 1,M } \mathbf{\text{do}} \\
&\quad \text{Initialize a random process $\mathcal{N}$ for action exploration}\\
&\quad \text{Receive initial observation state $s_1$}\\
&\quad \mathbf{\text{for}} \text{ t=1,T } \mathbf{\text{do}}\\
&\quad \quad \text{Select action $a_t = \mu (s_t|\theta^\mu) + \mathcal{N}_t$ acording to the current policy and exploration noise}\\
&\quad \quad \text{Execute action $a_t$ and observe reward $r_t$ and observe new state $s_{t+1}$}\\
&\quad \quad \text{Store transition $(s_t,a_t,r_t,s_{t+1})$ in $R$} \\
&\quad \quad \text{Sample a random minibatch of $N$ transitions $(s_t,a_t,r_t,s_{t+1})$ from $R$}\\
&\quad \quad \text{Set $y_i = r_i + \gamma Q'(s_{i+1},\mu'(s_{i+1}|\theta^{\mu'})|\theta^{Q'})$} \\
&\quad \quad \text{Update critic by minimizing the loss: $L = \frac{1}{N} \sum_{i} \big(y_i - Q(s_i,a_i|\theta^Q)\big)^2$} \\
&\quad \quad \text{Update the actor policy using the sampled policy gradient: } \\
&\quad \quad \quad \nabla_{\theta^\mu}J \approx \frac{1}{N} \sum_i \nabla_a Q(s,a\|\theta^Q) \big|_ {s=s_i, a = \mu(s_i)}\nabla_{\theta^\mu} \mu(s|\theta^\mu)|_ {s_i} \\
&\quad \quad \text{Update the target network: } \\
&\quad \quad \quad \theta^{Q'} \leftarrow \tau \theta^Q + (1-\tau) \theta^{Q'}\\
&\quad \quad \quad \theta^{\mu'} \leftarrow \tau \theta^\mu + (1-\tau) \theta^{\mu'} \\
&\quad \mathbf{ \text{end for}}\\
&\mathbf{ \text{end for}}\\
\end{align}
$$


 



$$
\begin{eqnarray*}
f(x) = \sum_{i=0}^{n} \frac{a_i}{1+x} \\
\textstyle f(x) = \textstyle \sum_{i=0}^{n} \frac{a_i}{1+x} \\
\scriptstyle f(x) = \scriptstyle \sum_{i=0}^{n} \frac{a_i}{1+x} \\
\scriptscriptstyle f(x) = \scriptscriptstyle \sum_{i=0}^{n} \frac{a_i}{1+x}
\end{eqnarray*}
$$

$$P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}$$

