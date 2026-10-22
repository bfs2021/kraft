# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/itsOmidKarami/kraft/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                         |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------------------- | -------: | -------: | ------: | --------: |
| src/kraft/\_\_init\_\_.py                    |        0 |        0 |    100% |           |
| src/kraft/\_\_main\_\_.py                    |        4 |        4 |      0% |       1-6 |
| src/kraft/adapters/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| src/kraft/adapters/agent.py                  |      353 |       15 |     96% |407, 506-507, 509, 748, 819-822, 898-901, 1162-1163 |
| src/kraft/adapters/artifact\_notes.py        |        2 |        0 |    100% |           |
| src/kraft/adapters/beads.py                  |       64 |       20 |     69% |61, 94-100, 134, 137-138, 194-202 |
| src/kraft/adapters/forge/\_\_init\_\_.py     |        8 |        0 |    100% |           |
| src/kraft/adapters/forge/ci.py               |       45 |        0 |    100% |           |
| src/kraft/adapters/forge/gh.py               |      258 |       14 |     95% |347, 373, 387-389, 467, 517, 579, 659-660, 662, 695, 720-721 |
| src/kraft/adapters/forge/git.py              |      216 |       14 |     94% |216-217, 234-235, 258-259, 291-293, 357-359, 560-561, 745 |
| src/kraft/adapters/forge/glab.py             |      345 |       18 |     95% |311-312, 476, 485, 508-509, 595, 608, 630, 686-687, 690, 738, 757, 828-829, 892-893 |
| src/kraft/adapters/forge/models.py           |      227 |        1 |     99% |       606 |
| src/kraft/adapters/forge/mr.py               |      127 |        3 |     98% |75, 204, 263 |
| src/kraft/adapters/forge/run.py              |      520 |       14 |     97% |567, 707-708, 762-764, 785, 1023-1024, 1054-1065, 1610, 1704 |
| src/kraft/adapters/hook\_install.py          |      232 |       10 |     96% |91, 186-189, 265-266, 291-292, 384 |
| src/kraft/adapters/profiles.py               |       35 |        0 |    100% |           |
| src/kraft/adapters/subprocess.py             |      496 |       16 |     97% |130, 304-305, 319-320, 347, 527, 579-580, 648, 693-694, 1119, 1227-1228, 1366 |
| src/kraft/addons/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/addons/config.py                   |      153 |        3 |     98% |152, 154, 166 |
| src/kraft/addons/fetch.py                    |      318 |       18 |     94% |99-100, 157-158, 185, 211-212, 254, 258, 397, 421, 513-514, 519-524 |
| src/kraft/addons/flow.py                     |      105 |        6 |     94% |89, 96, 98, 100, 136-137 |
| src/kraft/addons/inherit.py                  |      345 |        7 |     98% |66-67, 340, 427, 507, 514, 629 |
| src/kraft/addons/load.py                     |      472 |       39 |     92% |109, 204, 272-273, 412-413, 469-470, 505-506, 543-544, 572-573, 732-733, 762-763, 785-786, 807, 814-815, 865-866, 890, 895, 917-918, 920, 923-924, 926, 933-934, 950, 997, 1003-1004 |
| src/kraft/addons/manifest.py                 |      206 |        9 |     96% |122, 142, 148-150, 221, 258, 311-312 |
| src/kraft/addons/repo\_library.py            |      378 |       22 |     94% |88-89, 109, 115, 131-132, 225-226, 299-300, 314, 327, 345, 409-410, 429-430, 604-605, 655-656, 660 |
| src/kraft/addons/review.py                   |      292 |        9 |     97% |141-142, 189-190, 253, 371-374 |
| src/kraft/addons/update.py                   |      918 |       35 |     96% |107, 311-312, 330-331, 359-360, 383-384, 532-533, 579, 618-619, 657-658, 797, 839-840, 860-861, 1018-1019, 1082, 1088, 1274-1276, 1355-1356, 1558, 1575, 1584, 1674, 1812 |
| src/kraft/analytics.py                       |      275 |        7 |     97% |54-55, 176, 182, 471-473 |
| src/kraft/answers.py                         |      121 |        2 |     98% |  191, 194 |
| src/kraft/api/\_\_init\_\_.py                |       45 |        0 |    100% |           |
| src/kraft/api/apidocs.py                     |       24 |        0 |    100% |           |
| src/kraft/api/config\_check.py               |      428 |       29 |     93% |126, 203, 218-219, 293, 329-330, 340-341, 367, 370-371, 481, 537-540, 565, 619-620, 676-677, 694-695, 697, 703, 729-730, 840-841, 860 |
| src/kraft/api/deps.py                        |      496 |       27 |     95% |90-91, 181, 252-253, 547, 739, 742-744, 817-818, 830-831, 869-870, 879-880, 889-890, 1029-1030, 1065, 1068, 1071, 1094-1095 |
| src/kraft/api/item\_ids.py                   |       26 |        0 |    100% |           |
| src/kraft/api/perimeter.py                   |      133 |        2 |     98% |  271, 426 |
| src/kraft/api/routes/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| src/kraft/api/routes/admin.py                |       40 |        0 |    100% |           |
| src/kraft/api/routes/artifacts.py            |      274 |       10 |     96% |159, 296-303, 350-351, 412, 594 |
| src/kraft/api/routes/auth.py                 |       65 |        0 |    100% |           |
| src/kraft/api/routes/board.py                |      482 |        3 |     99% |902, 1001, 1004 |
| src/kraft/api/routes/check.py                |       20 |        0 |    100% |           |
| src/kraft/api/routes/drafts.py               |      300 |        9 |     97% |273, 289, 347-348, 354, 370, 387, 431, 542 |
| src/kraft/api/routes/gates.py                |      177 |        7 |     96% |128, 131, 145, 387-388, 471-472 |
| src/kraft/api/routes/harnesses.py            |       98 |        1 |     99% |       260 |
| src/kraft/api/routes/lifecycle.py            |     1040 |       51 |     95% |202, 205-206, 211-212, 316, 329, 413-416, 437-438, 459, 605, 693, 876, 939, 954, 985-996, 1032-1033, 1128, 1148, 1258-1259, 1269, 1443-1444, 1487, 1628, 1660, 1669, 1749, 1847-1848, 2064, 2069-2070, 2086, 2240-2241, 2326-2327, 2377-2378, 2380, 2587-2588, 2646 |
| src/kraft/api/routes/repos.py                |      341 |       16 |     95% |106-107, 226, 346-347, 363, 378-379, 447-448, 588-589, 712-713, 738-739 |
| src/kraft/api/routes/review.py               |      356 |       14 |     96% |86, 90, 101, 164, 189, 221, 260, 262, 272, 333, 514, 559-560, 656 |
| src/kraft/api/routes/search.py               |      158 |       11 |     93% |49-50, 84-87, 90, 136, 149-150, 189-190, 251 |
| src/kraft/api/routes/sessions.py             |      197 |       10 |     95% |137, 184, 188, 354, 429-431, 435, 437, 440 |
| src/kraft/api/routes/settings.py             |      489 |       29 |     94% |102-103, 145-146, 258-259, 268-269, 287-288, 365, 407-408, 563-566, 569, 612-613, 638-641, 644-645, 682-683, 745-746, 761-762, 794 |
| src/kraft/api/routes/storage.py              |       51 |        0 |    100% |           |
| src/kraft/api/routes/work\_items.py          |      476 |       36 |     92% |174, 476-479, 598-616, 700, 705, 822-823, 841-842, 1029, 1045, 1060, 1079-1080, 1178-1179, 1236-1237, 1242 |
| src/kraft/api/startup.py                     |      212 |        8 |     96% |114-115, 192-193, 198-199, 215-216 |
| src/kraft/apply.py                           |      117 |        6 |     95% |52, 79-80, 147-148, 199 |
| src/kraft/archive.py                         |       35 |        6 |     83% |     60-65 |
| src/kraft/auth.py                            |       75 |        8 |     89% |44, 48, 50-51, 96-99 |
| src/kraft/auto\_escalate\_delay.py           |       50 |        4 |     92% |   186-189 |
| src/kraft/automated\_review.py               |       12 |        0 |    100% |           |
| src/kraft/builtins.py                        |      788 |       51 |     94% |121-122, 130, 221, 287, 371, 385, 419, 423, 427, 433, 504-505, 525-526, 737, 836-837, 972, 991, 1049-1050, 1150-1151, 1340, 1459, 1494-1496, 1514-1515, 1603, 1609-1612, 1668-1669, 1681-1682, 1714-1715, 1758-1759, 1772, 1792-1793, 1808-1809, 2245-2248 |
| src/kraft/cap\_levels.py                     |       59 |        0 |    100% |           |
| src/kraft/capabilities.py                    |       38 |        0 |    100% |           |
| src/kraft/caps.py                            |      294 |       16 |     95% |141, 360, 386, 397, 409-410, 423, 520, 592, 630-632, 676-679 |
| src/kraft/cli/\_\_init\_\_.py                |       60 |       12 |     80% |103-109, 142-149, 156 |
| src/kraft/cli/addon.py                       |      592 |       32 |     95% |163-164, 179, 201, 216-217, 220, 253, 260, 262-263, 297, 307-315, 559, 564, 592, 662-663, 665, 669, 693, 725, 728-729, 851-852, 879-880, 919-920, 925 |
| src/kraft/cli/admin.py                       |      807 |       51 |     94% |95, 190-192, 210, 216-220, 229, 271, 307-308, 403-404, 412, 426, 541, 662, 689, 819-820, 912-913, 1031-1034, 1182-1183, 1313-1314, 1334, 1347-1348, 1350, 1360-1361, 1366, 1369, 1378-1384, 1423-1424, 1602, 1629 |
| src/kraft/cli/common.py                      |       27 |        0 |    100% |           |
| src/kraft/cli/item.py                        |      356 |        8 |     98% |32, 251, 335, 358, 395-396, 409, 468 |
| src/kraft/cli/repo.py                        |      378 |       17 |     96% |139, 147, 162, 175-176, 231, 233, 333, 364, 425, 429, 483, 492, 494, 499, 552-553 |
| src/kraft/cli/templates.py                   |      112 |        1 |     99% |       157 |
| src/kraft/cli/verify.py                      |      154 |        5 |     97% |133, 211-214 |
| src/kraft/cli/view.py                        |      301 |       10 |     97% |82, 269-270, 292, 302, 352-353, 389-395 |
| src/kraft/client/\_\_init\_\_.py             |        5 |        0 |    100% |           |
| src/kraft/client/actions.py                  |      225 |       24 |     89% |67, 183, 201, 244, 257, 325, 392, 414, 416, 442, 449-453, 531-532, 554, 582, 594, 630, 645, 670, 735 |
| src/kraft/client/context.py                  |       66 |        3 |     95% | 59-60, 78 |
| src/kraft/client/reads.py                    |      199 |        4 |     98% |311, 315, 431, 478 |
| src/kraft/client/transport.py                |      130 |       11 |     92% |101, 116-117, 134, 245-249, 261-262 |
| src/kraft/config.py                          |      676 |       17 |     97% |105, 128, 185-187, 203-205, 353, 609, 857, 901-902, 944, 1120-1121, 1208 |
| src/kraft/config\_schemas.py                 |       83 |        7 |     92% |   201-207 |
| src/kraft/console/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| src/kraft/console/acts.py                    |       92 |        1 |     99% |        38 |
| src/kraft/console/app.py                     |      463 |        4 |     99% |328-329, 385, 646 |
| src/kraft/console/chain.py                   |      187 |        4 |     98% |208, 219, 221-222 |
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
| src/kraft/console/screens/item.py            |      481 |       13 |     97% |393, 395-396, 446, 458-459, 482, 531, 621-622, 637, 696-697 |
| src/kraft/console/screens/item\_chain.py     |      137 |        4 |     97% |66-67, 169, 189 |
| src/kraft/console/screens/item\_menu.py      |       96 |        0 |    100% |           |
| src/kraft/console/screens/new\_item.py       |       74 |        1 |     99% |       141 |
| src/kraft/console/screens/repos.py           |       84 |        2 |     98% |   105-106 |
| src/kraft/console/screens/server.py          |      166 |        1 |     99% |       279 |
| src/kraft/console/status.py                  |       91 |        0 |    100% |           |
| src/kraft/console/tail.py                    |       49 |        1 |     98% |        68 |
| src/kraft/console/theme.py                   |        3 |        0 |    100% |           |
| src/kraft/console/words.py                   |      393 |        4 |     99% |109, 347, 470, 498 |
| src/kraft/db.py                              |      148 |        4 |     97% |1443, 1469-1471 |
| src/kraft/detect.py                          |     1085 |       64 |     94% |202, 357-359, 366-368, 455-462, 483, 578-579, 593, 601, 615, 635, 680, 686, 900, 913, 931, 949, 951, 1012-1013, 1087-1088, 1102, 1178, 1181, 1260, 1272, 1285, 1314-1316, 1326, 1467-1468, 1579, 1669-1670, 1672, 1845-1863, 1950, 2017 |
| src/kraft/doctor.py                          |      751 |       45 |     94% |173, 303-304, 383-384, 438, 442, 460, 464-465, 507, 554, 558, 604-605, 623-624, 712-713, 756-763, 813-814, 893-894, 1036-1037, 1090, 1102-1103, 1259-1260, 1343, 1361, 1374, 1384, 1426, 1434, 1530-1531, 1559, 1563-1564, 1590-1591 |
| src/kraft/drafts/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/drafts/areas.py                    |        6 |        0 |    100% |           |
| src/kraft/drafts/authored.py                 |      250 |       15 |     94% |85, 137, 161, 258, 304, 317, 322, 330, 343-344, 364, 369, 375, 393, 398 |
| src/kraft/drafts/config.py                   |      114 |        9 |     92% |47, 102-103, 121-122, 173-174, 176-177 |
| src/kraft/drafts/extending.py                |      402 |       16 |     96% |62, 137, 160, 240, 252, 285, 290, 316, 361, 377, 386, 418, 422, 437, 481, 623 |
| src/kraft/drafts/harnesses.py                |      324 |       21 |     94% |141, 159, 166, 240, 243, 245, 256, 258, 266, 270-273, 276, 280, 347, 358, 371-372, 442-444 |
| src/kraft/drafts/intake.py                   |      117 |        4 |     97% |47, 110-111, 181 |
| src/kraft/drafts/item.py                     |       88 |        2 |     98% |   88, 118 |
| src/kraft/drafts/ops.py                      |      801 |       74 |     91% |88, 138, 177-178, 199, 208, 210, 215, 221, 227, 233-234, 240-241, 257, 262, 356, 363-364, 420, 457, 459, 461, 501, 503, 540-541, 571, 602, 622, 644, 649-650, 655, 665, 678, 690-695, 707, 732, 762, 770, 776, 798, 824, 853, 857, 860, 887, 892, 939, 964, 982, 999, 1016, 1018, 1022-1024, 1027, 1030, 1045, 1048, 1075, 1081-1082, 1092, 1094, 1207-1208 |
| src/kraft/drafts/policy.py                   |      178 |       12 |     93% |58, 72, 89-91, 106, 174, 187-188, 248, 250, 253 |
| src/kraft/drafts/policy\_caps.py             |       60 |        3 |     95% | 43, 49-50 |
| src/kraft/drafts/preserve.py                 |      325 |       18 |     94% |101, 121, 124, 214-215, 250-251, 254, 383-390, 395, 505, 553 |
| src/kraft/drafts/repos.py                    |      162 |        8 |     95% |37, 45, 50, 78, 183, 226, 231-232 |
| src/kraft/drafts/resolve.py                  |      520 |       25 |     95% |122, 129-130, 186-187, 216, 222-223, 294-295, 390-391, 406-407, 446, 464, 625, 646, 799, 807-808, 823, 855, 887-888 |
| src/kraft/drafts/store.py                    |       78 |        0 |    100% |           |
| src/kraft/escalate.py                        |      219 |        5 |     98% |190, 296, 423, 605-616 |
| src/kraft/events.py                          |       31 |        0 |    100% |           |
| src/kraft/executor/\_\_init\_\_.py           |       10 |        0 |    100% |           |
| src/kraft/executor/context.py                |       60 |        2 |     97% |  243, 274 |
| src/kraft/executor/dispatch.py               |      916 |       24 |     97% |278, 347, 383-384, 515, 666, 669, 992-993, 1158-1159, 1191-1193, 1441-1442, 1454-1456, 1912, 1920, 2656, 3009, 3015 |
| src/kraft/executor/entry.py                  |      190 |        1 |     99% |       450 |
| src/kraft/executor/fallback.py               |       83 |        0 |    100% |           |
| src/kraft/executor/gates.py                  |      388 |       10 |     97% |241, 369, 372, 375, 380, 849, 866, 980-981, 1349 |
| src/kraft/executor/prompts.py                |      146 |        6 |     96% |131-138, 257 |
| src/kraft/executor/read\_only.py             |       82 |        2 |     98% |   79, 100 |
| src/kraft/executor/resuming.py               |       95 |        2 |     98% |  160, 203 |
| src/kraft/executor/retry.py                  |       26 |        0 |    100% |           |
| src/kraft/executor/round\_prompts.py         |       97 |        1 |     99% |       238 |
| src/kraft/executor/stops.py                  |      147 |        0 |    100% |           |
| src/kraft/executor/walk.py                   |      853 |       25 |     97% |96-97, 695, 762-763, 851, 947, 960, 1011, 1133-1138, 1574, 1620, 1634, 1707-1722, 1724, 1783, 2042, 2223, 2444, 2501, 2557 |
| src/kraft/findings.py                        |      112 |        0 |    100% |           |
| src/kraft/gate\_review.py                    |       99 |        5 |     95% |103-106, 111, 203, 380 |
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
| src/kraft/intake.py                          |      142 |       12 |     92% |100-102, 118, 161-162, 200-202, 243-248, 284 |
| src/kraft/intent.py                          |      198 |        9 |     95% |91-92, 186, 203, 264-265, 321-322, 339 |
| src/kraft/item\_paths.py                     |      301 |       59 |     80% |118, 372, 400, 418-419, 435-438, 450-466, 476-480, 483-485, 502-517, 524-525, 538, 549-552, 623-624, 646 |
| src/kraft/logs.py                            |      192 |       10 |     95% |105, 110, 127, 137, 154, 170-171, 179-180, 280 |
| src/kraft/mcp.py                             |      148 |        2 |     99% |   587-588 |
| src/kraft/mr\_poller.py                      |       68 |        9 |     87% |72-73, 85-86, 92, 127-130 |
| src/kraft/node\_runs.py                      |       78 |        3 |     96% |51, 103-104 |
| src/kraft/notify.py                          |      153 |       10 |     93% |184-185, 269-276, 289-292, 318 |
| src/kraft/overrides.py                       |       98 |        3 |     97% |116, 189-190 |
| src/kraft/paths.py                           |      105 |        0 |    100% |           |
| src/kraft/permission\_hooks.py               |       70 |        1 |     99% |        40 |
| src/kraft/permission\_rules.py               |       40 |        0 |    100% |           |
| src/kraft/pidfile.py                         |      125 |       19 |     85% |51-52, 57-58, 80-81, 117, 134, 145-146, 160-161, 169-170, 172, 196-197, 199-200 |
| src/kraft/policy.py                          |      826 |       24 |     97% |174, 296-297, 603, 608-609, 1324, 1516, 1750-1759, 1839, 1846, 1860, 1864-1868, 1873 |
| src/kraft/progress.py                        |      162 |        0 |    100% |           |
| src/kraft/rate\_limit\_retry.py              |       69 |        7 |     90% |165-167, 188-191 |
| src/kraft/registration.py                    |       59 |        0 |    100% |           |
| src/kraft/render.py                          |      284 |       24 |     92% |59-60, 105, 112, 396, 407, 422, 435, 441-445, 490-497, 548, 560, 586 |
| src/kraft/review.py                          |      183 |        5 |     97% |99, 227, 231, 279, 332 |
| src/kraft/review\_reply.py                   |       79 |        6 |     92% |96-97, 129-130, 135, 157 |
| src/kraft/skill.py                           |       88 |        8 |     91% |83-84, 113, 199, 204-205, 209-210 |
| src/kraft/start\_queue.py                    |      124 |        5 |     96% |122, 265-268 |
| src/kraft/storage.py                         |      276 |       14 |     95% |102-103, 132-133, 168-169, 185-186, 205, 365, 487-490 |
| src/kraft/store/\_\_init\_\_.py              |       13 |        0 |    100% |           |
| src/kraft/store/\_common.py                  |       51 |        2 |     96% |  137, 155 |
| src/kraft/store/budget.py                    |       69 |        0 |    100% |           |
| src/kraft/store/chain.py                     |      205 |        4 |     98% |375, 465-467 |
| src/kraft/store/counters.py                  |       55 |        0 |    100% |           |
| src/kraft/store/forks.py                     |       44 |        0 |    100% |           |
| src/kraft/store/gates.py                     |       75 |        0 |    100% |           |
| src/kraft/store/intake.py                    |       14 |        0 |    100% |           |
| src/kraft/store/passes.py                    |       57 |        0 |    100% |           |
| src/kraft/store/repos.py                     |       19 |        0 |    100% |           |
| src/kraft/store/review.py                    |      181 |        4 |     98% |212, 217, 224-225 |
| src/kraft/store/sessions.py                  |      197 |        0 |    100% |           |
| src/kraft/store/work\_items.py               |      361 |        5 |     99% |392, 438, 547, 743, 750 |
| src/kraft/templates/\_\_init\_\_.py          |        0 |        0 |    100% |           |
| src/kraft/templates/catalogue.py             |       86 |        0 |    100% |           |
| src/kraft/templates/environment.py           |      342 |        6 |     98% |545, 547, 613-614, 638-639 |
| src/kraft/templates/extension.py             |      216 |       10 |     95% |68-69, 133, 210, 230, 236, 248, 281, 291-292 |
| src/kraft/templates/forks.py                 |      100 |        0 |    100% |           |
| src/kraft/templates/library.py               |      928 |       23 |     98% |275-276, 324, 331, 520-521, 540, 562-563, 576-577, 627, 636-637, 774, 1234, 1300-1301, 1494, 1519-1521, 1591, 1716 |
| src/kraft/templates/models.py                |      745 |        7 |     99% |118, 121, 575, 753, 1423-1424, 1716 |
| src/kraft/templates/positions.py             |       57 |        0 |    100% |           |
| src/kraft/templates/retry.py                 |      105 |        7 |     93% |191, 201-203, 206-207, 214 |
| src/kraft/templates/revision.py              |      273 |        9 |     97% |219, 264, 318, 444, 530, 576-577, 579, 593 |
| src/kraft/triggers.py                        |       79 |        6 |     92% |107-108, 148-151 |
| src/kraft/update.py                          |      250 |       12 |     95% |80-81, 111-115, 120, 205-208, 363-364 |
| src/kraft/usage.py                           |      485 |       22 |     95% |119-120, 226, 357, 478, 538, 558-559, 562-563, 607, 686, 706-707, 978-979, 1084-1085, 1118-1119, 1269, 1281 |
| src/kraft/vocab/\_\_init\_\_.py              |        7 |        0 |    100% |           |
| src/kraft/vocab/display.py                   |       14 |        0 |    100% |           |
| src/kraft/vocab/events/\_\_init\_\_.py       |       32 |        0 |    100% |           |
| src/kraft/vocab/events/chain.py              |       34 |        0 |    100% |           |
| src/kraft/vocab/events/escalation.py         |       15 |        0 |    100% |           |
| src/kraft/vocab/events/forge.py              |       22 |        0 |    100% |           |
| src/kraft/vocab/events/gate.py               |       26 |        0 |    100% |           |
| src/kraft/vocab/events/limit.py              |       17 |        0 |    100% |           |
| src/kraft/vocab/events/sandbox.py            |       12 |        0 |    100% |           |
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
| src/kraft/waits.py                           |      106 |        7 |     93% |296-298, 308-311 |
| src/kraft/worker/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/worker/backends/\_\_init\_\_.py    |       36 |        0 |    100% |           |
| src/kraft/worker/backends/bwrap.py           |      320 |       26 |     92% |171, 212, 257-260, 275-276, 292, 314, 327, 375, 378, 382, 399, 413, 438, 516-517, 521, 558, 588, 611, 614-616 |
| src/kraft/worker/backends/docker.py          |      739 |       53 |     93% |326, 338-341, 353-360, 437, 552, 600, 609-610, 628, 658, 683-684, 711, 714-717, 786, 999-1000, 1110-1111, 1138, 1198, 1290-1293, 1386-1387, 1412-1413, 1456, 1520-1521, 1565, 1593, 1654-1655, 1694-1695, 1788-1789, 1815-1816 |
| src/kraft/worker/backends/docker\_forward.py |      136 |        7 |     95% |92-93, 95, 214-216, 224 |
| src/kraft/worker/backends/seatbelt.py        |      136 |        0 |    100% |           |
| src/kraft/worker/ca.py                       |      108 |        1 |     99% |       306 |
| src/kraft/worker/callback.py                 |       37 |        1 |     97% |        43 |
| src/kraft/worker/channel.py                  |      168 |        7 |     96% |161, 169, 203-204, 305, 331-332 |
| src/kraft/worker/egress.py                   |      470 |       36 |     92% |286-287, 293, 334-336, 355, 391, 397, 413-414, 424, 442, 444, 504, 559, 567-568, 675, 686, 709, 725, 749-750, 752-753, 765, 768, 798-799, 849-854 |
| src/kraft/worker/env.py                      |       11 |        0 |    100% |           |
| src/kraft/worker/host\_view.py               |      202 |       11 |     95% |157, 159-160, 166, 179, 196-197, 202, 206, 321, 333 |
| src/kraft/worker/inject.py                   |      238 |       18 |     92% |194, 214, 230, 241, 253, 351, 365, 374, 384, 390, 393, 407, 410, 415, 424-427 |
| src/kraft/worker/kit.py                      |      421 |       10 |     98% |124, 238-240, 430, 669-670, 672, 698, 732 |
| src/kraft/worker/mounts.py                   |      101 |        2 |     98% |   229-230 |
| src/kraft/worker/os\_init.py                 |      395 |      204 |     48% |75, 85, 89-100, 104-105, 109-183, 190-204, 223, 230-257, 268-269, 289-290, 321-322, 342, 348-350, 362, 390, 445-449, 473-474, 479-542, 546-550, 554 |
| src/kraft/worker/os\_seccomp.py              |       34 |        0 |    100% |           |
| src/kraft/worker/reattach.py                 |      336 |       30 |     91% |112-113, 122-123, 131-132, 152-153, 206-207, 319, 365, 377-378, 409, 482, 499-500, 508, 524-525, 705, 715-716, 794-798, 811-812, 829-830 |
| src/kraft/worker/refstore.py                 |      325 |        9 |     97% |210, 213, 222, 426-427, 589-590, 620, 643 |
| src/kraft/worker/sandbox.py                  |      159 |        5 |     97% |115, 159-160, 197, 222 |
| src/kraft/worker/session\_mcp.py             |       23 |        4 |     83% |45, 50-51, 53 |
| src/kraft/worker/shim.py                     |       10 |        0 |    100% |           |
| src/kraft/worker/steering.py                 |       37 |        0 |    100% |           |
| src/kraft/worker/tree\_walk.py               |       99 |       12 |     88% |71-72, 132-133, 135-136, 171-172, 181-182, 185-186 |
| src/kraft/worker/worktree\_read.py           |       90 |        8 |     91% |52, 165-167, 170-174, 182-183 |
| src/kraft/ws.py                              |       72 |        3 |     96% |     77-79 |
| **TOTAL**                                    | **47126** | **2203** | **95%** |           |


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