# CHANGELOG


## v1.0.0 (2024-11-23)

### :boom:

- :boom: Kick out old MCAP logger interface.
  ([`8b57557`](https://github.com/8-bit-hunters/mcap_logger/commit/8b57557ae92855e77134ccb5324e51da55e2d2bf))

- :boom: Make Topic attributes private and remove logger call from Topic.
  ([`58fb89b`](https://github.com/8-bit-hunters/mcap_logger/commit/58fb89ba3bb80bc034e43c4cfe09151f6f521fcd))

### :bug:

- :bug: Attribute error when Topic writer is none.
  ([`da33899`](https://github.com/8-bit-hunters/mcap_logger/commit/da3389929759de660743033b369ad1559f00a8c1))

### :egg:

- :egg: Add examples on how to use logging in application and library.
  ([`2c1ae97`](https://github.com/8-bit-hunters/mcap_logger/commit/2c1ae976f2a3bb447165c78ccb49ab9a653feabf))

- :egg: Add example of using TopicLogger.
  ([`3ec195d`](https://github.com/8-bit-hunters/mcap_logger/commit/3ec195d9b96299f62a9f71ba69cdfe3819502a7e))

- :egg: Add example of using the McapHandler.
  ([`ccdcfdd`](https://github.com/8-bit-hunters/mcap_logger/commit/ccdcfdd439f5f571d5c48e54852bae9e39a14555))

### :sparkles:

- :sparkles: Create TopicLogger class to handle data logging.
  ([`5d5f9d6`](https://github.com/8-bit-hunters/mcap_logger/commit/5d5f9d6c77ae1249844e47973012ddca4332632c))

- :sparkles: Create a logging handler for MCAP files.
  ([`803fd42`](https://github.com/8-bit-hunters/mcap_logger/commit/803fd42d1ac2766333117daef7747e31e38290a6))

### Other

- :construction_worker: Only publish to PyPI when new release is created
  ([`2582b2f`](https://github.com/8-bit-hunters/mcap_logger/commit/2582b2f9b8064b93fd47e41e082a57b98181c17a))

- :memo: Update links in README.
  ([`7868ace`](https://github.com/8-bit-hunters/mcap_logger/commit/7868ace32032f6c206ed7dc82056bae6fc8d9121))

- :memo: Add badges to README.
  ([`8966936`](https://github.com/8-bit-hunters/mcap_logger/commit/8966936900d0722648a22bb442aff6c3c8db1ab0))

- :memo: Fix documentation mistake.
  ([`26a7b8b`](https://github.com/8-bit-hunters/mcap_logger/commit/26a7b8b0a22acea6c7c84ea39e24d3ee69c1861f))

- :art: Change documentation Header style.
  ([`1cbc35b`](https://github.com/8-bit-hunters/mcap_logger/commit/1cbc35bb53748ee191c6274a1b23f919c8432dc7))

- :memo: Add tutorial on how to do library logging.
  ([`3a87810`](https://github.com/8-bit-hunters/mcap_logger/commit/3a8781064970a02690aa9184da9e0d4772efd5a3))

- :memo: Add tutorial to learn how to configure both console and MCAP logging for a logger.
  ([`0ef4494`](https://github.com/8-bit-hunters/mcap_logger/commit/0ef44947daec5c6abd8288e82ae6e114367bd68a))

- :memo: Create updated documentation for using the TopicLogger.
  ([`e6d2b2f`](https://github.com/8-bit-hunters/mcap_logger/commit/e6d2b2f17bf7306668ac2c646ba6909db0bc17b8))

- :truck: Move integration test resources to tests folder.
  ([`ef9d97c`](https://github.com/8-bit-hunters/mcap_logger/commit/ef9d97c3692fd7beba3cdff97ed7c12be2e75f33))

- :white_check_mark: Add integration test for data logging with TopicLogger.
  ([`4c19bf1`](https://github.com/8-bit-hunters/mcap_logger/commit/4c19bf19eff941bfbb3b55e0f4816326997dda6f))

- :wrench: Change Ruff configuration to exclude checks on ProtoBuf artifacts.
  ([`0c6cd16`](https://github.com/8-bit-hunters/mcap_logger/commit/0c6cd16cc33e2443fd1702130106f2d7a3222e10))

- :see_no_evil: Stop ignoring protobuf artifacts.
  ([`1c15b30`](https://github.com/8-bit-hunters/mcap_logger/commit/1c15b309a81d2d32a8a8dd23e6fbd617011ec69d))

- :memo: Add API reference for topic logger.
  ([`1e2f641`](https://github.com/8-bit-hunters/mcap_logger/commit/1e2f641ffd8b7f797bd283c822de159814adf17c))

- :bulb: Document the TopicLogger with docstrings.
  ([`1b12767`](https://github.com/8-bit-hunters/mcap_logger/commit/1b127670d963165a47cb29683e1fe5868f920e28))

- :recycle: Use time_ns() function instead of time().
  ([`285b60c`](https://github.com/8-bit-hunters/mcap_logger/commit/285b60ccb5664bfa6e41c83bae5eefa1c755a693))

- :art: Move Topic class to the same script as TopicLogger.
  ([`93d9f15`](https://github.com/8-bit-hunters/mcap_logger/commit/93d9f154d0ac68006ed832582d6730007f5adf5c))

- :memo: Added documentation about how to create your first log with McapHandler.
  ([`26d3096`](https://github.com/8-bit-hunters/mcap_logger/commit/26d309616f5654161c3222eb68e6b2cf32616907))

- :memo: Update documentation of API references.
  ([`a269048`](https://github.com/8-bit-hunters/mcap_logger/commit/a269048f28243ff5672154162c781752c32cb657))

- :construction_worker: add workflow for semantic versioning
  ([`124f1aa`](https://github.com/8-bit-hunters/mcap_logger/commit/124f1aa2e6133bfdc513d93016ce851d97c0a695))

- :wrench: configure semantic-release
  ([`7e62d9d`](https://github.com/8-bit-hunters/mcap_logger/commit/7e62d9dd7b4ccba8b119170dc0cd6d5d8e999ddd))

- :heavy_plus_sign: remove pypi-version dependency
  ([`4a5c631`](https://github.com/8-bit-hunters/mcap_logger/commit/4a5c631a7b9bed4a83bc2564fbe7d28f636e092c))

- :heavy_minus_sign: remove pypi-version dependency
  ([`6412f83`](https://github.com/8-bit-hunters/mcap_logger/commit/6412f832a42c5b39896479cf5230962c92bc1d89))


## v0.1.18 (2024-11-15)

### Other

- [pre-commit.ci] pre-commit autoupdate
  ([`f1b7187`](https://github.com/8-bit-hunters/mcap_logger/commit/f1b71879867fe9f14311606c7f096b280f6749c7))

updates: - [github.com/astral-sh/ruff-pre-commit: v0.7.2 →
  v0.7.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.7.2...v0.7.3)

- [pre-commit.ci] pre-commit autoupdate
  ([`f3a0192`](https://github.com/8-bit-hunters/mcap_logger/commit/f3a01921258589eccd23a0a66b519b5bd988a2b3))

updates: - [github.com/pre-commit/pre-commit-hooks: v2.3.0 →
  v5.0.0](https://github.com/pre-commit/pre-commit-hooks/compare/v2.3.0...v5.0.0) -
  [github.com/astral-sh/ruff-pre-commit: v0.6.9 →
  v0.7.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.6.9...v0.7.2)

- Ci: only trigger auto documentation on main branch
  ([`2be409c`](https://github.com/8-bit-hunters/mcap_logger/commit/2be409ced83e67b1e635d2dc185eb115b8052cbf))

- Chore: update project urls
  ([`b1cc2fd`](https://github.com/8-bit-hunters/mcap_logger/commit/b1cc2fd1e2bac033ce3e178aaa22a35dda48e205))

- Ci: auto publish documentation on github pages
  ([`b0df5d8`](https://github.com/8-bit-hunters/mcap_logger/commit/b0df5d849513bbe623bf82bb8fd26ee7a7fae654))

- Docs: create documentation with mkdocs
  ([`fe86327`](https://github.com/8-bit-hunters/mcap_logger/commit/fe863277de2f4b2fb0bee99790bf6100622ee13a))

- Docs: add tutorial for logging sensor data
  ([`fad79de`](https://github.com/8-bit-hunters/mcap_logger/commit/fad79dedfeee3db494755bcc9b2deb605bd6782f))

- Docs: add tutorials for installation and first log creation
  ([`6a6b2c2`](https://github.com/8-bit-hunters/mcap_logger/commit/6a6b2c2765bf2067b8675c0c9329857270f7b6f3))

- Docs: add github repo url link
  ([`ebdde12`](https://github.com/8-bit-hunters/mcap_logger/commit/ebdde1267721e34068a99f98eceb5433233f6960))

- Ci: run testing only if python files are changed
  ([`71a1482`](https://github.com/8-bit-hunters/mcap_logger/commit/71a1482524583c4900e7d4684d665831e6c814a0))

- Fix: wrong indentation in publishing workflow
  ([`72feee2`](https://github.com/8-bit-hunters/mcap_logger/commit/72feee2f34cdf69ef68410efa3eb11bcefb96450))

- Ci: add github workflow for publishing package
  ([`02b1a98`](https://github.com/8-bit-hunters/mcap_logger/commit/02b1a9806ed07ed786f3180d75df92dd4ff9a920))

- Ci: add github workflow for testing
  ([`d57245f`](https://github.com/8-bit-hunters/mcap_logger/commit/d57245f622fdfb0640e5213f5754d7a0e5ff777d))

- Ci: add test cases to the project
  ([`81b40a9`](https://github.com/8-bit-hunters/mcap_logger/commit/81b40a9e50753b28b3dfb19694d65495c8ea9e7c))

- Chore: create LICENSE
  ([`60e9fa4`](https://github.com/8-bit-hunters/mcap_logger/commit/60e9fa439b58358763701fa61ce8c20b22aa7550))

- Docs: add documentation to the package
  ([`a111f3c`](https://github.com/8-bit-hunters/mcap_logger/commit/a111f3c2abe21c007a787626c7e697c8baeb43b7))

- Fix: #2 console log shows the wrong function
  ([`f5c4653`](https://github.com/8-bit-hunters/mcap_logger/commit/f5c4653baf1fc02fae92a81e1188e98a417fbf40))

- Chore: fix ruff errors
  ([`c0b6fae`](https://github.com/8-bit-hunters/mcap_logger/commit/c0b6faeedcfef586bbe0e08eb43666b2c8ee30ed))

- Feat: log mcap messages on the console
  ([`cf55a16`](https://github.com/8-bit-hunters/mcap_logger/commit/cf55a1629bc26184c5b8a50deb16f4114f691661))

- Feat: define default logging path
  ([`a8e926a`](https://github.com/8-bit-hunters/mcap_logger/commit/a8e926ad5746c10462404bb26ca32edbc4b3f2f5))

- Refactor: change namings
  ([`b66f0be`](https://github.com/8-bit-hunters/mcap_logger/commit/b66f0be37bd8c2925fe6b72cd40254e1c4879588))

- Fix: wrong log level calls
  ([`1092efd`](https://github.com/8-bit-hunters/mcap_logger/commit/1092efd2d0f33364142f6294e4b7c793caf6e61b))

- Chore: add pre-commit and ruff formating
  ([`06ddc97`](https://github.com/8-bit-hunters/mcap_logger/commit/06ddc9715eb03167a106792b7c437e8236ab9c37))

- Feature: extend logging levels
  ([`698a3df`](https://github.com/8-bit-hunters/mcap_logger/commit/698a3dfe067e751847f5156818a262c492000a26))

- Refactor: create MCAP logger class to handle logs and topics
  ([`d78d49f`](https://github.com/8-bit-hunters/mcap_logger/commit/d78d49ff6d30cd4316f28ea67ceed849e630fa16))

- Refactor: create classes for logs and topics
  ([`849dce6`](https://github.com/8-bit-hunters/mcap_logger/commit/849dce60ca18daafe3b22858503c295ce8254cb7))

- Feat: sensor example with logging using protobuf
  ([`51330da`](https://github.com/8-bit-hunters/mcap_logger/commit/51330da705dbc030eddef4cb9610281e49d64db9))

- Feat: use protobuf
  ([`ba00e07`](https://github.com/8-bit-hunters/mcap_logger/commit/ba00e07b68316304a6d9d932555888f4393a1202))

- Feat: logging sample data into mcap file
  ([`43c56d1`](https://github.com/8-bit-hunters/mcap_logger/commit/43c56d101aa0ab4fb48afbb968694e1c026613d6))
