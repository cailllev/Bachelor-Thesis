# ping call stack

in ``_initIroha()``, in ``/app/src/diva-api.js`` on line 244<br>
``DivaApi._timeout('pingBlockchain', () => DivaApi._pingBlockchain(), MS_1M)``


## getting called from ...

* ``_initIroha()``<br>
function on line 223 in ``/app/src/diva-api.js``<br>
getting called from ``make()``

  * ``make()``<br>
function on line 73 in ``/app/src/diva-api.js``<br>
getting called from ``main.js`` on line 31

    * ``main.js``<br>
script at ``/app/main.js``<br>
getting called from entrypoint.sh

      * ``entrypoint.sh``<br>
script at ``/``<br>
getting called from Dockerfile

        * ``Dockerfile``<br>
script at ``/``<br>
is excecuted when ``docker up``


## variable definitions

- ``DivaApi``<br>
is the class (this)

- ``DivaApi.iroha``<br>
defined in ``_init_Iroha()``<br>
``DivaApi.iroha = await Iroha.make(DivaApi.torii, DivaApi.creator, DivaApi.pathIroha)``

- ``Iroha.make()``<br>
in ``/app/src/iroha.js``<br>
creates new Iroha object


## calls ...

* ``_timeout(...)``	<br>
function on line 454 in ``/app/src/diva-api.js``<br>
TL;DR fancy wrapper for setting a timeout, then calling the function

  * ``_pingBlockchain()``<br>
funtion on line 438 in ``/app/src/diva-api.js``<br>
calls  ``DivaApi.iroha.setAccountDetail(DivaApi.creator, 'ping', Math.floor(Date.now() / 1000))``

    * ``setAccountDetail(...)``<br>
function on line 242 in ``/app/src/iroha.js``<br>
calls ``return commands.setAccountDetail({...},{...})``<br>
``import { commands, queries } from 'iroha-helpers'``

      * ``commands``<br>
defines exports for iroha-helpers<br>
overview [iroha-helpers](https://www.npmjs.com/package/iroha-helpers#commands)<br>
``npm pack iroha-helpers`` to download source<br><br>
in ``/package/lib/index.js`` (this is the entrypoint)<br>
``var tslib_1 = require("tslib");``<br>
``var commands_1 = tslib_1.__importDefault(require("./commands"));``<br>
``exports.commands = commands_1["default"];``<br>
(tslib is just a fancy wrapper of ts import functionality)

        * ``commands.setAccountDetail(...)``<br>
export on line 287 from ``/package/lib/commands``<br>
exports ``setAccountDetail``, this means ``_pingBlockchain() -> iroha.setAccountDetail(...)`` (from iroha.js ) ``-> setAccountDetail(...)`` (from  /package/lib/commands/index.js)<br>
calls ``command`` from ``/package/lib/commands/index.js``<br>

          * ``command`` <br>
funtion on line 20 from ``/package/lib/commands/index.js``<br>
takes given options or uses default<br>
calls ``util_1.signWithArrayOfKeys(...)``<br>
calls ``util_1.sendTransaction(...)``<br>
``util_1 = require("../util")``

            * ``util.signWithArrayOfKeys(...)``<br>
function on line 126 from ``/package/lib/util.js``<br>
``signWithArrayOfKeys(...) {... txHelper_1["default"].sign(...) ...}`` 

              * ``txHelper_1``<br>
var on line 5 from ``/package/lib/util.js``<br>
``txHelper_1 = tslib_1.__importDefault(require("./txHelper"));``

                * ``txHelper.js``<br>
exports ``sign`` for ``util.signWithArrayOfKeys`` on line 145

                  * ``sign(...)``<br>
function on line 99 in ``/package/lib/txHelper.js``<br>
calls ``hash(...)``<br>
calls ``cryptoHelper_1["default"].sign(...)``<br>
gets private key from ``buffer_1.Buffer.frompublic

                    * ``hash(transaction)``<br>
function on line 91 in ``/package/lib/txHelper.js``<br>
hashes ``transaction.getPayload()`` with ``js-sha3``

                    * ``cryptoHelper_1``<br>
variable defined in ``/package/lib/txHelper.js`` on line 12<br>
``var cryptoHelper_1 = tslib_1.__importDefault(require("./cryptoHelper"))``


                      * ``cryptoHelper.js``<br>
TODO

            * ``util_1.sendTransaction(...)``<br>
function on line 105 from ``/package/lib/util.js``<br>
returns a Promise after ``_listToTorii(...)`` has resolved

              * ``_listToTorii(..)``<br>
function on line 7 from ``/package/lib/util.js``<br>
calls ``hash(...)`` from ``txHelper.js`` (see above)



			






 

