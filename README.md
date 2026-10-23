# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/itsOmidKarami/kraft/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                         |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------------------- | -------: | -------: | ------: | --------: |
| src/kraft/\_\_init\_\_.py                    |        0 |        0 |    100% |           |
| src/kraft/\_\_main\_\_.py                    |        4 |        4 |      0% |       1-6 |
| src/kraft/adapters/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| src/kraft/adapters/agent.py                  |      367 |       16 |     96% |417, 516-517, 519, 775, 846-849, 925-928, 1048, 1220-1221 |
| src/kraft/adapters/artifact\_notes.py        |        2 |        0 |    100% |           |
| src/kraft/adapters/beads.py                  |       64 |       20 |     69% |61, 94-100, 134, 137-138, 194-202 |
| src/kraft/adapters/forge/\_\_init\_\_.py     |        8 |        0 |    100% |           |
| src/kraft/adapters/forge/ci.py               |       45 |        0 |    100% |           |
| src/kraft/adapters/forge/gh.py               |      339 |       19 |     94% |465, 511-512, 594-596, 674, 724, 755-756, 782-783, 842, 922-923, 925, 958, 983-984 |
| src/kraft/adapters/forge/git.py              |      223 |       15 |     93% |217-218, 235-236, 259-260, 292-294, 358-360, 555-562, 770 |
| src/kraft/adapters/forge/glab.py             |      412 |       20 |     95% |373-374, 538, 547, 570-571, 663, 719, 741, 804-805, 844-845, 847, 895, 914, 985-986, 1056-1057 |
| src/kraft/adapters/forge/models.py           |      272 |        1 |     99% |       730 |
| src/kraft/adapters/forge/mr.py               |      147 |        3 |     98% |77, 206, 265 |
| src/kraft/adapters/forge/run.py              |      696 |       35 |     95% |255-259, 315, 553-557, 651, 921, 1090-1091, 1152-1154, 1184, 1288, 1307-1308, 1320, 1464-1465, 1500-1511, 2119, 2220-2226, 2246 |
| src/kraft/adapters/forge/settle.py           |       51 |        0 |    100% |           |
| src/kraft/adapters/hook\_install.py          |      232 |       10 |     96% |91, 186-189, 265-266, 291-292, 384 |
| src/kraft/adapters/profiles.py               |       35 |        0 |    100% |           |
| src/kraft/adapters/subprocess.py             |      518 |       15 |     97% |134, 308-309, 533, 585-586, 654, 699-700, 1144, 1252-1253, 1299-1300, 1408 |
| src/kraft/addons/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/addons/config.py                   |      153 |        3 |     98% |152, 154, 166 |
| src/kraft/addons/fetch.py                    |      318 |       18 |     94% |99-100, 157-158, 185, 211-212, 254, 258, 397, 421, 513-514, 519-524 |
| src/kraft/addons/flow.py                     |      105 |        6 |     94% |89, 96, 98, 100, 136-137 |
| src/kraft/addons/inherit.py                  |      345 |        7 |     98% |66-67, 340, 427, 507, 514, 629 |
| src/kraft/addons/load.py                     |      472 |       39 |     92% |109, 204, 272-273, 412-413, 469-470, 505-506, 543-544, 572-573, 732-733, 762-763, 785-786, 807, 814-815, 865-866, 890, 895, 917-918, 920, 923-924, 926, 933-934, 950, 997, 1003-1004 |
| src/kraft/addons/manifest.py                 |      206 |        9 |     96% |122, 142, 148-150, 221, 258, 311-312 |
| src/kraft/addons/repo\_library.py            |      378 |       22 |     94% |88-89, 109, 115, 131-132, 225-226, 299-300, 314, 327, 345, 409-410, 429-430, 604-605, 655-656, 660 |
| src/kraft/addons/review.py                   |      298 |        9 |     97% |146-147, 194-195, 258, 387-390 |
| src/kraft/addons/update.py                   |      918 |       35 |     96% |107, 311-312, 330-331, 359-360, 383-384, 532-533, 579, 618-619, 657-658, 797, 839-840, 860-861, 1018-1019, 1082, 1088, 1274-1276, 1355-1356, 1558, 1575, 1584, 1674, 1812 |
| src/kraft/analytics.py                       |      275 |        7 |     97% |54-55, 176, 182, 471-473 |
| src/kraft/answers.py                         |      124 |        3 |     98% |191, 194, 273 |
| src/kraft/api/\_\_init\_\_.py                |       45 |        0 |    100% |           |
| src/kraft/api/apidocs.py                     |       24 |        0 |    100% |           |
| src/kraft/api/config\_check.py               |      445 |       32 |     93% |129, 206, 221-222, 296, 332-333, 343-344, 370, 373-374, 447-448, 475, 514, 570-573, 598, 652-653, 709-710, 727-728, 730, 736, 762-763, 873-874, 893 |
| src/kraft/api/deps.py                        |      501 |       27 |     95% |91-92, 189, 260-261, 556, 748, 751-753, 826-827, 839-840, 878-879, 888-889, 898-899, 1038-1039, 1074, 1077, 1080, 1103-1104 |
| src/kraft/api/item\_ids.py                   |       26 |        0 |    100% |           |
| src/kraft/api/perimeter.py                   |      133 |        2 |     98% |  271, 426 |
| src/kraft/api/routes/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| src/kraft/api/routes/admin.py                |       88 |        1 |     99% |       134 |
| src/kraft/api/routes/artifacts.py            |      275 |       10 |     96% |159, 296-303, 350-351, 412, 597 |
| src/kraft/api/routes/auth.py                 |       65 |        0 |    100% |           |
| src/kraft/api/routes/board.py                |      482 |        3 |     99% |904, 1003, 1006 |
| src/kraft/api/routes/check.py                |       20 |        0 |    100% |           |
| src/kraft/api/routes/drafts.py               |      300 |        9 |     97% |273, 289, 347-348, 354, 370, 387, 431, 542 |
| src/kraft/api/routes/gates.py                |      187 |        7 |     96% |134, 137, 151, 409-410, 494-495 |
| src/kraft/api/routes/harnesses.py            |       98 |        1 |     99% |       260 |
| src/kraft/api/routes/lifecycle.py            |     1139 |       57 |     95% |187-188, 193-194, 254, 270, 361, 374, 458-461, 482-483, 504, 650, 738, 921, 984, 999, 1030-1041, 1077-1078, 1173, 1193, 1304-1305, 1315, 1489-1490, 1533, 1615, 1617, 1662, 1780, 1812, 1821, 1901, 1999-2000, 2073, 2239, 2244-2245, 2261, 2360, 2435-2436, 2521-2522, 2572-2573, 2575, 2784-2785, 2843 |
| src/kraft/api/routes/repos.py                |      341 |       16 |     95% |106-107, 226, 346-347, 363, 378-379, 447-448, 588-589, 712-713, 738-739 |
| src/kraft/api/routes/review.py               |      359 |       14 |     96% |86, 90, 101, 164, 189, 221, 260, 262, 272, 333, 519, 564-565, 661 |
| src/kraft/api/routes/search.py               |      158 |       11 |     93% |49-50, 84-87, 90, 136, 149-150, 189-190, 251 |
| src/kraft/api/routes/sessions.py             |      197 |       10 |     95% |137, 184, 188, 354, 429-431, 435, 437, 440 |
| src/kraft/api/routes/settings.py             |      512 |       29 |     94% |102-103, 145-146, 258-259, 268-269, 287-288, 366, 408-409, 566-569, 572, 615-616, 677-680, 683-684, 721-722, 784-785, 800-801, 833 |
| src/kraft/api/routes/storage.py              |       51 |        0 |    100% |           |
| src/kraft/api/routes/work\_items.py          |      481 |       36 |     93% |175, 480-483, 602-620, 704, 709, 826-827, 845-846, 1036, 1052, 1067, 1086-1087, 1193-1194, 1251-1252, 1257 |
| src/kraft/api/routes/workers.py              |      108 |        9 |     92% |51-52, 76-80, 102, 114-115 |
| src/kraft/api/startup.py                     |      253 |        9 |     96% |186, 262-263, 340-341, 346-347, 363-364 |
| src/kraft/apply.py                           |      135 |        6 |     96% |53, 80-81, 148-149, 217 |
| src/kraft/archive.py                         |       35 |        6 |     83% |     60-65 |
| src/kraft/auth.py                            |       75 |        8 |     89% |44, 48, 50-51, 96-99 |
| src/kraft/auto\_escalate\_delay.py           |       52 |        5 |     90% |72, 188-191 |
| src/kraft/automated\_review.py               |       21 |        1 |     95% |        62 |
| src/kraft/builtins.py                        |      790 |       51 |     94% |121-122, 130, 221, 287, 371, 385, 419, 423, 427, 433, 504-505, 525-526, 737, 836-837, 972, 991, 1049-1050, 1150-1151, 1340, 1459, 1494-1496, 1514-1515, 1603, 1609-1612, 1668-1669, 1681-1682, 1714-1715, 1758-1759, 1772, 1792-1793, 1808-1809, 2256-2259 |
| src/kraft/cap\_levels.py                     |       59 |        0 |    100% |           |
| src/kraft/capabilities.py                    |       38 |        0 |    100% |           |
| src/kraft/caps.py                            |      296 |       16 |     95% |143, 362, 388, 399, 411-412, 425, 522, 594, 632-634, 678-681 |
| src/kraft/cli/\_\_init\_\_.py                |       60 |       12 |     80% |103-109, 142-149, 156 |
| src/kraft/cli/addon.py                       |      592 |       32 |     95% |163-164, 179, 201, 216-217, 220, 253, 260, 262-263, 297, 307-315, 559, 564, 592, 662-663, 665, 669, 693, 725, 728-729, 851-852, 879-880, 919-920, 925 |
| src/kraft/cli/admin.py                       |      975 |       88 |     91% |99, 194-196, 214, 220-224, 233, 275, 311-312, 407-408, 416, 430, 545, 667, 694, 824-825, 917-918, 1036-1039, 1187-1188, 1318-1319, 1339, 1352-1353, 1355, 1365-1366, 1371, 1374, 1379-1382, 1386-1389, 1400-1401, 1416-1417, 1434-1435, 1444-1445, 1451-1455, 1480-1482, 1491, 1502-1507, 1519-1525, 1574-1575, 1785, 1808-1810, 1829, 1840, 1854-1858, 1879, 1885, 1909 |
| src/kraft/cli/common.py                      |       27 |        0 |    100% |           |
| src/kraft/cli/item.py                        |      380 |        9 |     98% |32, 264, 277, 375, 398, 436-437, 450, 509 |
| src/kraft/cli/repo.py                        |      378 |       17 |     96% |139, 147, 162, 175-176, 231, 233, 333, 364, 425, 429, 483, 492, 494, 499, 552-553 |
| src/kraft/cli/templates.py                   |      112 |        1 |     99% |       157 |
| src/kraft/cli/verify.py                      |      154 |        5 |     97% |133, 211-214 |
| src/kraft/cli/view.py                        |      301 |       10 |     97% |82, 272-273, 295, 305, 355-356, 392-398 |
| src/kraft/cli/worker.py                      |       94 |       22 |     77% |22-24, 81, 96, 99-119, 124 |
| src/kraft/client/\_\_init\_\_.py             |        5 |        0 |    100% |           |
| src/kraft/client/actions.py                  |      253 |       34 |     87% |68, 184, 202, 245, 258, 331, 398, 423, 425, 427, 434-435, 464, 473-477, 555-556, 578, 606, 618, 656, 672, 698, 763, 786, 791-794, 799, 805 |
| src/kraft/client/context.py                  |       66 |        3 |     95% | 59-60, 78 |
| src/kraft/client/reads.py                    |      199 |        4 |     98% |314, 318, 434, 481 |
| src/kraft/client/transport.py                |      131 |       11 |     92% |101, 116-117, 134, 247-251, 263-264 |
| src/kraft/config.py                          |      714 |       17 |     98% |107, 130, 187-189, 205-207, 357, 613, 861, 905-906, 948, 1124-1125, 1212 |
| src/kraft/config\_schemas.py                 |       83 |        7 |     92% |   202-208 |
| src/kraft/console/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| src/kraft/console/acts.py                    |       92 |        1 |     99% |        38 |
| src/kraft/console/app.py                     |      463 |        4 |     99% |328-329, 385, 646 |
| src/kraft/console/chain.py                   |      187 |        4 |     98% |209, 220, 222-223 |
| src/kraft/console/dialogs.py                 |      212 |        2 |     99% |  230, 369 |
| src/kraft/console/live.py                    |      105 |        1 |     99% |       114 |
| src/kraft/console/moments.py                 |       78 |        0 |    100% |           |
| src/kraft/console/output.py                  |       53 |        0 |    100% |           |
| src/kraft/console/panels.py                  |       97 |        4 |     96% |59, 157-159 |
| src/kraft/console/prompt.py                  |      137 |        4 |     97% |57, 125, 144, 187 |
| src/kraft/console/pulse.py                   |      119 |        0 |    100% |           |
| src/kraft/console/runner.py                  |      113 |        0 |    100% |           |
| src/kraft/console/screens/\_\_init\_\_.py    |       19 |        1 |     95% |        28 |
| src/kraft/console/screens/addons.py          |      236 |        5 |     98% |298-301, 306, 395 |
| src/kraft/console/screens/board.py           |      392 |        9 |     98% |374, 377, 388, 515, 551-555 |
| src/kraft/console/screens/item.py            |      483 |       10 |     98% |451, 463-464, 487, 536, 626-627, 642, 701-702 |
| src/kraft/console/screens/item\_chain.py     |      137 |        5 |     96% |66-67, 82, 169, 189 |
| src/kraft/console/screens/item\_menu.py      |       97 |        0 |    100% |           |
| src/kraft/console/screens/new\_item.py       |       74 |        1 |     99% |       141 |
| src/kraft/console/screens/repos.py           |       84 |        2 |     98% |   105-106 |
| src/kraft/console/screens/server.py          |      166 |        1 |     99% |       279 |
| src/kraft/console/status.py                  |       91 |        0 |    100% |           |
| src/kraft/console/tail.py                    |       49 |        1 |     98% |        68 |
| src/kraft/console/theme.py                   |        3 |        0 |    100% |           |
| src/kraft/console/words.py                   |      405 |        4 |     99% |109, 347, 470, 498 |
| src/kraft/db.py                              |      148 |        4 |     97% |1443, 1469-1471 |
| src/kraft/detect.py                          |     1085 |       64 |     94% |202, 357-359, 366-368, 455-462, 483, 578-579, 593, 601, 615, 635, 680, 686, 900, 913, 931, 949, 951, 1012-1013, 1087-1088, 1102, 1178, 1181, 1260, 1272, 1285, 1314-1316, 1326, 1467-1468, 1579, 1669-1670, 1672, 1845-1863, 1950, 2017 |
| src/kraft/doctor.py                          |      778 |       49 |     94% |104-105, 181, 279-280, 340-341, 420-421, 475, 479, 497, 501-502, 544, 591, 595, 641-642, 660-661, 749-750, 793-800, 850-851, 930-931, 1073-1074, 1127, 1139-1140, 1296-1297, 1380, 1398, 1411, 1421, 1463, 1471, 1567-1568, 1596, 1600-1601, 1627-1628 |
| src/kraft/drafts/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/drafts/areas.py                    |        6 |        0 |    100% |           |
| src/kraft/drafts/authored.py                 |      250 |       15 |     94% |85, 137, 161, 258, 304, 317, 322, 330, 343-344, 364, 369, 375, 393, 398 |
| src/kraft/drafts/config.py                   |      114 |        9 |     92% |47, 102-103, 121-122, 173-174, 176-177 |
| src/kraft/drafts/extending.py                |      402 |       16 |     96% |62, 137, 160, 240, 252, 285, 290, 316, 361, 377, 386, 418, 422, 437, 481, 623 |
| src/kraft/drafts/harnesses.py                |      324 |       21 |     94% |141, 159, 166, 240, 243, 245, 256, 258, 266, 270-273, 276, 280, 347, 358, 371-372, 442-444 |
| src/kraft/drafts/intake.py                   |      117 |        4 |     97% |47, 110-111, 181 |
| src/kraft/drafts/item.py                     |       88 |        2 |     98% |   88, 118 |
| src/kraft/drafts/ops.py                      |      843 |       75 |     91% |94, 144, 183-184, 205, 214, 216, 221, 227, 233, 239-240, 246-247, 263, 268, 362, 369-370, 426, 463, 465, 467, 507, 509, 546-547, 577, 608, 628, 650, 655-656, 661, 671, 708, 755, 771-776, 788, 813, 843, 851, 857, 879, 905, 934, 938, 941, 968, 973, 1020, 1045, 1063, 1080, 1097, 1099, 1103-1105, 1108, 1111, 1126, 1129, 1156, 1162-1163, 1173, 1175, 1288-1289 |
| src/kraft/drafts/policy.py                   |      178 |       12 |     93% |58, 72, 89-91, 106, 174, 187-188, 248, 250, 253 |
| src/kraft/drafts/policy\_caps.py             |       60 |        3 |     95% | 43, 49-50 |
| src/kraft/drafts/preserve.py                 |      325 |       18 |     94% |101, 121, 124, 214-215, 250-251, 254, 383-390, 395, 505, 553 |
| src/kraft/drafts/repos.py                    |      162 |        8 |     95% |37, 45, 50, 78, 183, 226, 231-232 |
| src/kraft/drafts/resolve.py                  |      524 |       25 |     95% |123, 130-131, 187-188, 217, 223-224, 295-296, 391-392, 407-408, 447, 465, 632, 653, 808, 816-817, 832, 864, 896-897 |
| src/kraft/drafts/store.py                    |       78 |        0 |    100% |           |
| src/kraft/escalate.py                        |      230 |        5 |     98% |212, 318, 466, 649-660 |
| src/kraft/events.py                          |       31 |        0 |    100% |           |
| src/kraft/executor/\_\_init\_\_.py           |       10 |        0 |    100% |           |
| src/kraft/executor/context.py                |       63 |        2 |     97% |  266, 297 |
| src/kraft/executor/dispatch.py               |      942 |       24 |     97% |281, 370, 406-407, 557, 708, 711, 1054-1055, 1231-1232, 1264-1266, 1526-1527, 1539-1541, 2005, 2013, 2756, 3109, 3115 |
| src/kraft/executor/entry.py                  |      204 |        1 |     99% |       484 |
| src/kraft/executor/fallback.py               |       83 |        0 |    100% |           |
| src/kraft/executor/gates.py                  |      397 |       10 |     97% |250, 377, 380, 383, 388, 878, 895, 1009-1010, 1409 |
| src/kraft/executor/prompts.py                |      151 |        6 |     96% |134-141, 260 |
| src/kraft/executor/read\_only.py             |       82 |        2 |     98% |   79, 100 |
| src/kraft/executor/resuming.py               |       95 |        2 |     98% |  160, 203 |
| src/kraft/executor/retry.py                  |       26 |        0 |    100% |           |
| src/kraft/executor/round\_prompts.py         |      135 |        5 |     96% |275, 303, 324-325, 340 |
| src/kraft/executor/stops.py                  |      147 |        0 |    100% |           |
| src/kraft/executor/walk.py                   |      960 |       30 |     97% |101-102, 727, 796-797, 885, 985, 998, 1044, 1223-1224, 1267-1268, 1271, 1384-1389, 1820, 1866, 1880, 1953-1968, 1970, 2029, 2288, 2469, 2708, 2765, 2821 |
| src/kraft/findings.py                        |      112 |        0 |    100% |           |
| src/kraft/gate\_review.py                    |       99 |        5 |     95% |103-106, 111, 208, 386 |
| src/kraft/grants.py                          |       64 |        0 |    100% |           |
| src/kraft/harness.py                         |      335 |       18 |     95% |194, 202, 217, 238, 258, 265, 272, 284, 404, 563, 565, 567, 576, 595-596, 633-635 |
| src/kraft/ids.py                             |       29 |        0 |    100% |           |
| src/kraft/index/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| src/kraft/index/chunk.py                     |       44 |        1 |     98% |        65 |
| src/kraft/index/db.py                        |       68 |        5 |     93% |158-159, 168-170 |
| src/kraft/index/embed.py                     |       75 |        9 |     88% |42-43, 80, 100-102, 122-124 |
| src/kraft/index/ingest.py                    |      262 |        9 |     97% |236-237, 358, 448-450, 560-562 |
| src/kraft/index/service.py                   |      470 |       31 |     93% |141-143, 159, 164, 219, 291-293, 330, 349-351, 404-405, 410, 413-414, 642, 693-694, 710, 728, 732-733, 928, 931, 937, 960, 963, 1021 |
| src/kraft/init.py                            |       51 |        2 |     96% |     62-64 |
| src/kraft/inplace/\_\_init\_\_.py            |       37 |        0 |    100% |           |
| src/kraft/inplace/base.py                    |      127 |        5 |     96% |96-98, 252, 267 |
| src/kraft/inplace/rebasing.py                |      122 |        9 |     93% |71, 103, 110-111, 118, 138-139, 239-240 |
| src/kraft/inplace/taking.py                  |      146 |        4 |     97% |43, 50, 64, 221 |
| src/kraft/inplace/task\_check.py             |      207 |        3 |     99% |188, 354-355 |
| src/kraft/intake.py                          |      144 |       13 |     91% |58, 102-104, 120, 163-164, 202-204, 245-250, 287 |
| src/kraft/intent.py                          |      198 |        9 |     95% |91-92, 186, 203, 264-265, 321-322, 339 |
| src/kraft/item\_paths.py                     |      302 |       59 |     80% |118, 378, 406, 424-425, 441-444, 456-472, 482-486, 489-491, 508-523, 530-531, 544, 555-558, 629-630, 652 |
| src/kraft/logs.py                            |      192 |       10 |     95% |105, 110, 127, 137, 154, 170-171, 179-180, 280 |
| src/kraft/mcp.py                             |      157 |        2 |     99% |   637-638 |
| src/kraft/mr\_poller.py                      |       68 |        9 |     87% |72-73, 85-86, 92, 127-130 |
| src/kraft/node\_runs.py                      |      104 |        5 |     95% |51, 116-117, 154-155 |
| src/kraft/notify.py                          |      153 |       10 |     93% |184-185, 269-276, 289-292, 318 |
| src/kraft/overrides.py                       |      109 |        3 |     97% |125, 200-201 |
| src/kraft/paths.py                           |      105 |        0 |    100% |           |
| src/kraft/permission\_hooks.py               |       70 |        1 |     99% |        40 |
| src/kraft/permission\_rules.py               |       40 |        0 |    100% |           |
| src/kraft/pidfile.py                         |      125 |       19 |     85% |51-52, 57-58, 80-81, 117, 134, 145-146, 160-161, 169-170, 172, 196-197, 199-200 |
| src/kraft/policy.py                          |      828 |       24 |     97% |174, 297-298, 608, 613-614, 1329, 1521, 1755-1764, 1844, 1851, 1865, 1869-1873, 1878 |
| src/kraft/progress.py                        |      162 |        0 |    100% |           |
| src/kraft/rate\_limit\_retry.py              |       71 |        8 |     89% |56, 167-169, 190-193 |
| src/kraft/registration.py                    |       59 |        0 |    100% |           |
| src/kraft/remote/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/remote/check.py                    |       54 |        6 |     89% |80-81, 84-85, 89, 92 |
| src/kraft/remote/hub.py                      |      141 |       13 |     91% |115-117, 120-121, 149, 183, 187-190, 210-211 |
| src/kraft/remote/machine.py                  |       64 |       12 |     81% |38, 100-113 |
| src/kraft/remote/protocol.py                 |       85 |        4 |     95% |85, 129-130, 138 |
| src/kraft/remote/registry.py                 |       99 |        0 |    100% |           |
| src/kraft/remote/transport.py                |       57 |        5 |     91% |36-37, 45, 72-73 |
| src/kraft/render.py                          |      286 |       24 |     92% |59-60, 105, 112, 396, 407, 422, 435, 441-445, 496-503, 554, 566, 592 |
| src/kraft/review.py                          |      183 |        5 |     97% |99, 227, 231, 279, 332 |
| src/kraft/review\_reply.py                   |       80 |        6 |     92% |96-97, 129-130, 135, 157 |
| src/kraft/reviewed\_head.py                  |      101 |        2 |     98% |   226-227 |
| src/kraft/skill.py                           |       88 |        8 |     91% |83-84, 113, 199, 204-205, 209-210 |
| src/kraft/start\_check.py                    |       39 |        6 |     85% |40-42, 49-50, 58 |
| src/kraft/start\_queue.py                    |      126 |        5 |     96% |124, 267-270 |
| src/kraft/storage.py                         |      276 |       14 |     95% |102-103, 132-133, 168-169, 185-186, 205, 365, 487-490 |
| src/kraft/store/\_\_init\_\_.py              |       13 |        0 |    100% |           |
| src/kraft/store/\_common.py                  |       51 |        2 |     96% |  137, 155 |
| src/kraft/store/budget.py                    |       69 |        0 |    100% |           |
| src/kraft/store/chain.py                     |      208 |        4 |     98% |411, 501-503 |
| src/kraft/store/counters.py                  |       55 |        0 |    100% |           |
| src/kraft/store/forks.py                     |       43 |        0 |    100% |           |
| src/kraft/store/gates.py                     |       89 |        0 |    100% |           |
| src/kraft/store/intake.py                    |       14 |        0 |    100% |           |
| src/kraft/store/passes.py                    |       62 |        0 |    100% |           |
| src/kraft/store/repos.py                     |       19 |        0 |    100% |           |
| src/kraft/store/review.py                    |      181 |        4 |     98% |212, 217, 224-225 |
| src/kraft/store/sessions.py                  |      197 |        0 |    100% |           |
| src/kraft/store/work\_items.py               |      366 |        5 |     99% |392, 438, 547, 743, 750 |
| src/kraft/templates/\_\_init\_\_.py          |        0 |        0 |    100% |           |
| src/kraft/templates/catalogue.py             |       86 |        0 |    100% |           |
| src/kraft/templates/environment.py           |      342 |        6 |     98% |545, 547, 613-614, 638-639 |
| src/kraft/templates/extension.py             |      216 |       10 |     95% |68-69, 133, 210, 230, 236, 248, 281, 291-292 |
| src/kraft/templates/forks.py                 |      100 |        0 |    100% |           |
| src/kraft/templates/library.py               |      928 |       23 |     98% |275-276, 324, 331, 520-521, 540, 562-563, 576-577, 627, 636-637, 774, 1234, 1300-1301, 1494, 1519-1521, 1591, 1716 |
| src/kraft/templates/models.py                |      807 |        7 |     99% |121, 124, 623, 811, 1568-1569, 1873 |
| src/kraft/templates/positions.py             |       57 |        0 |    100% |           |
| src/kraft/templates/retry.py                 |      105 |        7 |     93% |193, 203-205, 208-209, 216 |
| src/kraft/templates/revision.py              |      273 |        9 |     97% |219, 264, 318, 445, 531, 577-578, 580, 594 |
| src/kraft/triggers.py                        |       79 |        6 |     92% |107-108, 148-151 |
| src/kraft/update.py                          |      315 |       20 |     94% |80-81, 111-115, 120, 203-204, 233-236, 342-343, 345, 446-447, 554, 574, 586 |
| src/kraft/usage.py                           |      485 |       22 |     95% |119-120, 226, 357, 478, 538, 558-559, 562-563, 607, 686, 706-707, 978-979, 1084-1085, 1118-1119, 1269, 1281 |
| src/kraft/vocab/\_\_init\_\_.py              |        7 |        0 |    100% |           |
| src/kraft/vocab/display.py                   |       14 |        0 |    100% |           |
| src/kraft/vocab/events/\_\_init\_\_.py       |       32 |        0 |    100% |           |
| src/kraft/vocab/events/chain.py              |       34 |        0 |    100% |           |
| src/kraft/vocab/events/escalation.py         |       15 |        0 |    100% |           |
| src/kraft/vocab/events/forge.py              |       26 |        0 |    100% |           |
| src/kraft/vocab/events/gate.py               |       26 |        0 |    100% |           |
| src/kraft/vocab/events/limit.py              |       17 |        0 |    100% |           |
| src/kraft/vocab/events/sandbox.py            |       14 |        0 |    100% |           |
| src/kraft/vocab/events/session.py            |       17 |        0 |    100% |           |
| src/kraft/vocab/events/settings.py           |       14 |        0 |    100% |           |
| src/kraft/vocab/events/traits.py             |        8 |        0 |    100% |           |
| src/kraft/vocab/events/work\_item.py         |       35 |        0 |    100% |           |
| src/kraft/vocab/review.py                    |       22 |        0 |    100% |           |
| src/kraft/vocab/session.py                   |       43 |        0 |    100% |           |
| src/kraft/vocab/sql.py                       |       29 |        0 |    100% |           |
| src/kraft/vocab/stop.py                      |       27 |        0 |    100% |           |
| src/kraft/vocab/total.py                     |       11 |        0 |    100% |           |
| src/kraft/vocab/work\_item.py                |       98 |        0 |    100% |           |
| src/kraft/waits.py                           |      113 |        8 |     93% |260, 333-335, 345-348 |
| src/kraft/when\_free.py                      |      426 |       33 |     92% |76, 155-157, 196-198, 247, 393, 395, 442-444, 560-562, 578-580, 594, 609-615, 623-636, 644, 805 |
| src/kraft/worker/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/worker/backends/\_\_init\_\_.py    |       36 |        0 |    100% |           |
| src/kraft/worker/backends/bwrap.py           |      325 |       26 |     92% |171, 212, 257-260, 275-276, 292, 314, 327, 379, 382, 386, 403, 417, 442, 526-527, 531, 563, 595, 622, 625-627 |
| src/kraft/worker/backends/docker.py          |      739 |       53 |     93% |326, 338-341, 353-360, 437, 552, 600, 609-610, 628, 658, 683-684, 711, 714-717, 786, 1000-1001, 1111-1112, 1139, 1199, 1291-1294, 1387-1388, 1413-1414, 1457, 1521-1522, 1566, 1594, 1663-1664, 1703-1704, 1797-1798, 1824-1825 |
| src/kraft/worker/backends/docker\_forward.py |      136 |        7 |     95% |92-93, 95, 214-216, 224 |
| src/kraft/worker/backends/seatbelt.py        |      150 |        3 |     98% |   365-367 |
| src/kraft/worker/ca.py                       |      108 |        1 |     99% |       306 |
| src/kraft/worker/callback.py                 |       37 |        1 |     97% |        43 |
| src/kraft/worker/channel.py                  |      170 |        7 |     96% |164, 172, 206-207, 308, 334-335 |
| src/kraft/worker/egress.py                   |      470 |       36 |     92% |286-287, 293, 334-336, 355, 391, 397, 413-414, 424, 442, 444, 504, 559, 567-568, 675, 686, 709, 725, 749-750, 752-753, 765, 768, 798-799, 849-854 |
| src/kraft/worker/env.py                      |       11 |        0 |    100% |           |
| src/kraft/worker/host\_view.py               |      202 |       11 |     95% |157, 159-160, 166, 179, 196-197, 202, 206, 321, 333 |
| src/kraft/worker/inject.py                   |      238 |       18 |     92% |194, 214, 230, 241, 253, 351, 365, 374, 384, 390, 393, 407, 410, 415, 424-427 |
| src/kraft/worker/kit.py                      |      421 |       10 |     98% |124, 238-240, 430, 669-670, 672, 698, 732 |
| src/kraft/worker/mounts.py                   |      102 |        2 |     98% |   230-231 |
| src/kraft/worker/os\_init.py                 |      395 |      204 |     48% |75, 85, 89-100, 104-105, 109-183, 190-205, 224, 231-258, 269-270, 290-291, 322-323, 343, 349-351, 363, 391, 446-450, 474-475, 480-543, 547-551, 555 |
| src/kraft/worker/os\_seccomp.py              |       34 |        0 |    100% |           |
| src/kraft/worker/reattach.py                 |      363 |       31 |     91% |114-115, 124-125, 133-134, 154-155, 238-239, 352, 398, 410-411, 442, 515, 532-533, 541, 557-558, 624, 755, 765-766, 844-848, 861-862, 879-880 |
| src/kraft/worker/refstore.py                 |      325 |        9 |     97% |210, 213, 222, 426-427, 589-590, 620, 643 |
| src/kraft/worker/sandbox.py                  |      159 |        5 |     97% |116, 160-161, 198, 223 |
| src/kraft/worker/session\_mcp.py             |       23 |        4 |     83% |45, 50-51, 53 |
| src/kraft/worker/shim.py                     |       10 |        0 |    100% |           |
| src/kraft/worker/steering.py                 |       37 |        0 |    100% |           |
| src/kraft/worker/tree\_walk.py               |       99 |       12 |     88% |71-72, 132-133, 135-136, 171-172, 181-182, 185-186 |
| src/kraft/worker/worktree\_read.py           |       90 |        8 |     91% |52, 165-167, 170-174, 182-183 |
| src/kraft/ws.py                              |       72 |        3 |     96% |     77-79 |
| **TOTAL**                                    | **50004** | **2435** | **95%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/itsOmidKarami/kraft/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/itsOmidKarami/kraft/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/itsOmidKarami/kraft/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/itsOmidKarami/kraft/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FitsOmidKarami%2Fkraft%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/itsOmidKarami/kraft/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.