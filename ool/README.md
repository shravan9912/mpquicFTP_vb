# OOL #

Code base of online-offline learning (OOL) framework (folders of ChangeDetection and Learning) applying for the multipath transport protocol (the other folders). It is worth to mention that OOL is not limited to the demonstrated use case but rather any other scenarios that require the online learning. 

The specific routine of OOL is as following. ChangeDetection module can take any type of time-series data as input and detect the change point (gradual, sudden types, etc.). The change detection has two types, i.e., online type and offline type. The online type is subject to the OOL use case, where the data is assumed to arrive sequentially. On the contrary, the offline type takes the whole dataset as the input. The offline type can be regarded as the baseline of the online type.

The learning module can take the learning model (h5f file) and train over the experience (csv file), within any training steps, to obtain the updated model. In the offline phase, given a set of user collected experiences, the defined number of training steps and any random learning model, the user hosts each experience over each learning module concurrently. A meta model is eventually obtained over these concurrent learning modules, i.e., defined number of training steps away from the convergence of these concurrent learning modules. In the online phase, once the changedetection module reports the change, simply select one meta model (h5f file) and then train over the ongoing experince.  

The use case module (e.g., multipath networking module), change detection module, and the learning module should run in different process. As a more pratical point, the user might consider allocate relatively large stack spaces for these modules. 
