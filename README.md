# ortools-service
A service for or-tools based on gRPC with some added utilities.
The ortools service is intended to facilitate the creation of optimization models in a scalable, modular, and compositional approach.

This repository include some client utils and examples for formulating and sending linear programming requests to the ortools service.

## Why or-tools Service for Python?

If you are developing optimization models in python (e.g. for asset operation and planning management like I do), you may be familliar with algebraic modeling languages (AML) that are used to facilititate the defenition and solving of large scale optimization problems.
These tools bridge the gap between the object oriented model defenition and standard format of optimization problems used in optimization solvers. 
Also, they alllow the optimization model to be solver agnostic.


In Python, Pyomo is very popular library for the optimization AML. It provides very convenient tools for object oriented model defenition.
However, in terms of performance and especially for larger models, pyomo tends to show not ideal. 
A good alternative in terms of performance, particularly for MILP type problems, is the google ORtools. 
It is implemented in Cpp, but also provides a python interface library. 
This is why for real applications ortools is preffered to pyomo (IMO).

A tiny problem here is that ortools does not provide the same level of convenience in terms of model defenition as Pyomo, especially if one would want to use it as a service. 
**But why to use these AML tools as a service?** 
A typical approach would be to install the pyomo library (or ortools python library) in the same environment that we develop the model, but this would mean that the solver(s), also need to be in the same package, which is not ideal for larger applications. A service, in contrast, allows to define the optimization as a data object that is passed to a remote solver, decoupling the defenition and solution.

OR-tools natively supports the service approach via gRPC, which is great. But the model defenition is *"kinda"* limited (an experienced optimization expert may disagree); you cannot define "expressions" as common in Pyomo, you have to know the indecies of your variables in the constraints, etc. **But we could add these features to our ortools service.** 

Another feature, which would be useful, is to define a bigger model that is composed of smaller ones, with having the parts defined separately, but at the same time, having them able to **refer** to each other, and sometimes without being explicitly introduced, i.e. *add this constraint to all my parents children!*


## How to Setup and Use the Ortools service:
If you are courisous about this app, and are thinking to take it for a little spin, then great!
The first requirement to that is to have the server (on AWS) up and running! for that, send an email to sakha00@ucr.edu to have it up.
Next you should be able to run the sample client example in main/client/client_main.py.
Finally, you could also try and create your own  optimizations with or without cross-referencing between the models.