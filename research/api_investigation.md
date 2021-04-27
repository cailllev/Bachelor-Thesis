# ping call stack

in ``_initIroha()``, in ``/app/src/diva-api.js`` on line 244
``DivaApi._timeout('pingBlockchain', () => DivaApi._pingBlockchain(), MS_1M)``


## getting called from ...

- ``_initIroha()``
function on line 223 in ``/app/src/diva-api.js``
getting called from ``make()``

  - ``make()``
function on line 73 in ``/app/src/diva-api.js``
getting called from ``main.js`` on line 31

    - ``main.js``
script at ``/app/main.js``
getting called from entrypoint.sh

      - ``entrypoint.sh``
script at /
getting called from Dockerfile

        - ``Dockerfile``
script at /
is excecuted when ``docker up``


## variable definitions

- ``DivaApi``
is the class (this)

- ``DivaApi.iroha``
defined in ``_init_Iroha()``
``DivaApi.iroha = await Iroha.make(DivaApi.torii, DivaApi.creator, DivaApi.pathIroha)``

- ``Iroha.make()``
in ``/app/src/iroha.js``
creates new Iroha object


## calls ...

- ``_timeout(...)``	
function on line 454 in ``/app/src/diva-api.js``
TL;DR fancy wrapper for setting a timeout, then calling the function

  - ``_pingBlockchain()``
funtion on line 438 in ``/app/src/diva-api.js``
calls  ``DivaApi.iroha.setAccountDetail(DivaApi.creator, 'ping', Math.floor(Date.now() / 1000))``

    - ``setAccountDetail(...)``
function on line 242 in ``/app/src/iroha.js``
calls ``return commands.setAccountDetail({...},{...})``
``import { commands, queries } from 'iroha-helpers'``

    - ``commands``
defines exports for iroha-helpers
overview [iroha-helpers](https://www.npmjs.com/package/iroha-helpers#commands)
``npm pack iroha-helpers`` to download source<br><br>

in ``/package/lib/index.js`` (this is the entrypoint)
``var tslib_1 = require("tslib");``
``var commands_1 = tslib_1.__importDefault(require("./commands"));``
``exports.commands = commands_1["default"];``
(tslib is just a fancy wrapper of ts import functionality)

      - ``commands.setAccountDetail(...)``
export on line 287 from ``/package/lib/commands``
exports ``setAccountDetail``, this means ``_pingBlockchain() -> iroha.setAccountDetail(...)`` (from iroha.js ) ``-> setAccountDetail(...)`` (from  /package/lib/commands/index.js)
calls ``command`` from ``/package/lib/commands/index.js``

        - ``command`` 
funtion on line 20 from ``/package/lib/commands/index.js``
takes given options or uses default
calls ``util_1.signWithArrayOfKeys(...)``
calls ``util_1.sendTransaction(...)``
``util_1 = require("../util")``

          - ``util.signWithArrayOfKeys(...)``
function on line 126 from ``/package/lib/util.js``
``signWithArrayOfKeys(...) {... txHelper_1["default"].sign(...) ...}`` 

            - ``txHelper_1``
var on line 5 from ``/package/lib/util.js``
``txHelper_1 = tslib_1.__importDefault(require("./txHelper"));``

              - ``txHelper.js``
exports ``sign`` for ``util.signWithArrayOfKeys`` on line 145

                - ``sign(...)``
function on line 99 in ``/package/lib/txHelper.js``
calls ``hash(...)``
calls ``cryptoHelper_1["default"].sign(...)``
gets private key from ``buffer_1.Buffer.frompublic

                  - ``hash(transaction)``
function on line 91 in ``/package/lib/txHelper.js``
hashes ``transaction.getPayload()`` with ``js-sha3``

                  - ``cryptoHelper_1``
variable defined in ``/package/lib/txHelper.js`` on line 12
``var cryptoHelper_1 = tslib_1.__importDefault(require("./cryptoHelper"))``


                    - ``cryptoHelper.js``
TODO

          - ``util_1.sendTransaction(...)``
function on line 105 from ``/package/lib/util.js``
returns a Promise after ``_listToTorii(...)`` has resolved

            - ``_listToTorii(..)``
function on line 7 from ``/package/lib/util.js``
calls ```hash(...)`` from ``txHelper.js`` (see above)



			






 

