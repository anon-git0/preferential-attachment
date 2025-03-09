# preferential-attachment
A description of type competition in preferential attachment networks and a simulation of the model.

The 'preferential attachment' assumption is that new nodes are more likely to connect to existing ones that already have a lot of connections. This assumption makes sense in a lot of real life scenarios – for example, if the network represents a social network, where nodes are persons and the connections represent friendships, then it is a reasonable assumption that people who already have a lot of friends are likely to rapidly gain more friends or followers in the future – they may be people with large social circles, or famous influences, celebrities or politicians.
In our preferential attachment model, at each time step, a single vertex joins the network and makes two connections with other vertices at random; the probability that it connects to each vertex is proportional to its degree (how many connections it has already) – for example, a vertex with degree ten is five times as likely to be chosen as the parent to connect to as a vertex with degree two. This is repeated many times, and the network grows.
## Type competition
We are interested in the competition between vertex ‘types’. Each vertex is given a type when it joins the network, based on the types of its parents. For example, types may be named ‘Coca-Cola’ and ‘Pepsi’, and represent the brand preferences of the persons in the network, where we assume that your brand preference is influenced by those around you.
The exact rule for how your type is determined can be specified by the user. In our program, we will allow the user to specify, for each possible combination of a pair of parents, which parent's type is inherited by the new vertex.

## Example
An interesting example is the case of a three-type 'rock-paper-scissors' model. When the new vertex has two differing parent types, it inherits the type that would win in a rock-paper-scissors contest. In this model, the proportions of each type present do not converge to $1/3$ as $n \to \infty;$ instead, the proportions oscillate around $1/3$ for all time.

See below for an example of this result from the program.

![3_types](https://github.com/user-attachments/assets/521d8cc9-e72e-49c9-a542-d30ef8478276)

Here, we exhibit another example with five competing types, using the rock-paper-scissors-lizard-Spock rules of Sam Kass.

![5_types](https://github.com/user-attachments/assets/e5cf6245-391b-4db6-a251-57c0136acf4f)

## Algorithm
In this section (more mathematically intensive), we explain how the .py program operates.

Note that the degree of a vertex/node is the number of connections that vertex makes.
Also note that vertices are allowed to choose the same parent twice - this is not unintended behaviour, and is common and accepted in the literature. Not allowing this will typically not change any long-term behaviour, and just make mathematical arguments more difficult and clunky.

The key point is that it is not necessary to keep track of the entire structure of the network - all its nodes and their connections and types. We only need to track **the total degree of each type**; as in, the degrees of all vertices of that type added together, which I will name $A_k$ for any type $k.$ This makes computation much faster and more efficient than if the entire network is tracked.

When a new vertex joins the network, for each of its two independent parent choices, the probability that the parent is of a certain type $k$ will be equal to $A_k$ divided by the total degree of all vertices in the network. This calculation does not require any knowledge of the exact network structure. Additionally, when the new vertex takes a new type, it only depends on the types of its parents. Then, the total degree of each parent type increases by one, because the new vertex connects to each of them. Additionally, whatever the type of the new vertex is, the total degree of that type increases by two, as the new vertex has made two connections.
After these updates are made, the program is ready for the next time step.
