# ping call stack

in ``_initIroha()``, in ``/app/src/diva-api.js`` on line 244
``DivaApi._timeout('pingBlockchain', () => DivaApi._pingBlockchain(), MS_1M)``


## getting called from ...

### ``_initIroha()``
function on line 223 in ``/app/src/diva-api.js``
getting called from ``make()``

### ``make()``
function on line 73 in ``/app/src/diva-api.js``
getting called from ``main.js`` on line 31

### ``main.js``
script at ``/app/main.js``
getting called from entrypoint.sh

### ``entrypoint.sh``
script at /
getting called from Dockerfile

### ``Dockerfile``
script at /
is excecuted when ``docker up``


## variable definitions

### ``DivaApi``
is the class (this)

### ``DivaApi.iroha``
defined in ``_init_Iroha()``
``DivaApi.iroha = await Iroha.make(DivaApi.torii, DivaApi.creator, DivaApi.pathIroha)``

### ``Iroha.make()``
in ``/app/src/iroha.js``
creates new Iroha object


## calls ...

### ``_timeout()``	
function on line 454 in ``/app/src/diva-api.js``
TL;DR fancy wrapper for setting a timeout, then calling the function

### ``_pingBlockchain()``
funtion on line 438 in ``/app/src/diva-api.js``
calls  ``DivaApi.iroha.setAccountDetail(DivaApi.creator, 'ping', Math.floor(Date.now() / 1000))``

### ``setAccountDetail()``
function on line 242 in ``/app/src/iroha.js``
calls ``return commands.setAccountDetail({...},{...})``

### commands
from [iroha-helpers](https://www.npmjs.com/package/iroha-helpers#commands)
``npm i iroha-helpers``







