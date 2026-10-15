# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/itsOmidKarami/kraft/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                         |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------------------- | -------: | -------: | ------: | --------: |
| src/kraft/\_\_init\_\_.py                    |        0 |        0 |    100% |           |
| src/kraft/\_\_main\_\_.py                    |        4 |        4 |      0% |       1-6 |
| src/kraft/adapters/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| src/kraft/adapters/agent.py                  |      337 |       15 |     96% |388, 487-488, 490, 725, 796-799, 872-875, 1117-1118 |
| src/kraft/adapters/artifact\_notes.py        |        2 |        0 |    100% |           |
| src/kraft/adapters/beads.py                  |       62 |       19 |     69% |82-88, 122, 125-126, 182-190 |
| src/kraft/adapters/forge/\_\_init\_\_.py     |        8 |        0 |    100% |           |
| src/kraft/adapters/forge/ci.py               |       45 |        0 |    100% |           |
| src/kraft/adapters/forge/gh.py               |      156 |       11 |     93% |253, 277, 283-293, 371, 422 |
| src/kraft/adapters/forge/git.py              |      215 |       15 |     93% |216-217, 234-235, 258-259, 291-293, 357-359, 554-561, 739 |
| src/kraft/adapters/forge/glab.py             |      180 |       10 |     94% |239-240, 327, 336, 359-360, 426, 429, 442, 464 |
| src/kraft/adapters/forge/models.py           |      181 |        0 |    100% |           |
| src/kraft/adapters/forge/mr.py               |      125 |        5 |     96% |75, 204, 256, 322-323 |
| src/kraft/adapters/forge/run.py              |      453 |       11 |     98% |427, 611-613, 860-861, 891-902, 1407, 1501 |
| src/kraft/adapters/hook\_install.py          |      232 |       10 |     96% |91, 185-188, 264-265, 290-291, 380 |
| src/kraft/adapters/profiles.py               |       35 |        0 |    100% |           |
| src/kraft/adapters/subprocess.py             |      436 |       13 |     97% |129, 303-304, 318-319, 346, 559-560, 628, 1029, 1055-1056, 1246 |
| src/kraft/addons/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/addons/config.py                   |      152 |        3 |     98% |150, 152, 164 |
| src/kraft/addons/fetch.py                    |      318 |       19 |     94% |99-100, 157-158, 185, 211-212, 254, 258, 324, 397, 421, 513-514, 519-524 |
| src/kraft/addons/load.py                     |      391 |       35 |     91% |91, 227-228, 346-347, 393-394, 405-406, 439-440, 468-469, 577-578, 597, 602-603, 630, 653-654, 678, 683, 705-706, 708, 711-712, 714, 721-722, 738, 785, 791-792 |
| src/kraft/addons/manifest.py                 |      184 |        9 |     95% |115, 135, 141-143, 211, 241, 282-283 |
| src/kraft/addons/repo\_library.py            |      349 |       20 |     94% |88-89, 109, 115, 131-132, 225-226, 297-298, 317, 381-382, 401-402, 543-544, 594-595, 599 |
| src/kraft/addons/review.py                   |      225 |        9 |     96% |119-120, 176-177, 251-254, 257 |
| src/kraft/addons/update.py                   |      472 |       20 |     96% |103, 212-213, 219-220, 328-329, 337-338, 384, 423-424, 462-463, 487, 611, 619, 821, 876-877 |
| src/kraft/analytics.py                       |      275 |        7 |     97% |54-55, 176, 182, 471-473 |
| src/kraft/api/\_\_init\_\_.py                |       45 |        0 |    100% |           |
| src/kraft/api/apidocs.py                     |       24 |        0 |    100% |           |
| src/kraft/api/config\_check.py               |      410 |       26 |     94% |125, 202, 217-218, 292, 328-329, 339-340, 471, 527-530, 555, 609-610, 666-667, 684-685, 687, 693, 719-720, 797-798, 817 |
| src/kraft/api/deps.py                        |      472 |       24 |     95% |90-91, 223-224, 518, 710, 713-715, 788-789, 801-802, 840-841, 850-851, 984-985, 1020, 1023, 1026, 1049-1050 |
| src/kraft/api/item\_ids.py                   |       26 |        0 |    100% |           |
| src/kraft/api/perimeter.py                   |      133 |        2 |     98% |  271, 426 |
| src/kraft/api/routes/\_\_init\_\_.py         |        0 |        0 |    100% |           |
| src/kraft/api/routes/admin.py                |       40 |        0 |    100% |           |
| src/kraft/api/routes/artifacts.py            |      260 |       10 |     96% |150, 271-278, 325-326, 387, 566 |
| src/kraft/api/routes/auth.py                 |       65 |        0 |    100% |           |
| src/kraft/api/routes/board.py                |      464 |        3 |     99% |853, 952, 955 |
| src/kraft/api/routes/check.py                |       20 |        0 |    100% |           |
| src/kraft/api/routes/drafts.py               |      295 |        9 |     97% |271, 287, 345-346, 352, 368, 385, 424, 535 |
| src/kraft/api/routes/gates.py                |      141 |        5 |     96% |122, 125, 139, 382-383 |
| src/kraft/api/routes/harnesses.py            |       98 |        1 |     99% |       258 |
| src/kraft/api/routes/lifecycle.py            |      935 |       47 |     95% |182, 185-186, 191-192, 296, 309, 393-396, 417-418, 439, 558, 646, 829, 880, 925, 945, 1055-1056, 1066, 1229-1230, 1354, 1386, 1395, 1475, 1569-1570, 1786, 1791-1792, 1808, 1930, 1960-1961, 2024, 2044-2045, 2090-2091, 2093, 2275-2276, 2328 |
| src/kraft/api/routes/repos.py                |      333 |       16 |     95% |105-106, 225, 339-340, 356, 371-372, 440-441, 573-574, 695-696, 721-722 |
| src/kraft/api/routes/review.py               |      328 |       15 |     95% |86, 90, 101, 164, 189, 221, 260, 262, 272, 333, 460-461, 511-512, 608 |
| src/kraft/api/routes/search.py               |      152 |       11 |     93% |48-49, 83-86, 89, 135, 148-149, 188-189, 246 |
| src/kraft/api/routes/sessions.py             |      197 |       10 |     95% |137, 184, 188, 354, 429-431, 435, 437, 440 |
| src/kraft/api/routes/settings.py             |      479 |       31 |     94% |92-93, 135-136, 204-205, 220-221, 230-231, 249-250, 326, 368-369, 524-527, 530, 573-574, 599-602, 605-606, 643-644, 692-693, 708-709, 741 |
| src/kraft/api/routes/storage.py              |       48 |        0 |    100% |           |
| src/kraft/api/routes/work\_items.py          |      448 |       31 |     93% |171, 466-469, 585-603, 683, 806-807, 994, 1011, 1030-1031, 1133, 1190-1191, 1196 |
| src/kraft/api/startup.py                     |      201 |        4 |     98% |112-113, 202-203 |
| src/kraft/apply.py                           |      117 |        6 |     95% |52, 79-80, 147-148, 199 |
| src/kraft/archive.py                         |       35 |        6 |     83% |     60-65 |
| src/kraft/auth.py                            |       75 |        8 |     89% |44, 48, 50-51, 96-99 |
| src/kraft/auto\_escalate\_delay.py           |       50 |        4 |     92% |   186-189 |
| src/kraft/automated\_review.py               |       12 |        0 |    100% |           |
| src/kraft/builtins.py                        |      747 |       47 |     94% |114-115, 123, 214, 280, 364, 378, 412, 416, 420, 426, 497-498, 518-519, 606, 797-798, 931, 950, 1008-1009, 1108-1109, 1281, 1398, 1433-1435, 1453-1454, 1534, 1540-1543, 1599-1600, 1612-1613, 1656, 1664-1665, 1708-1709, 2116-2119 |
| src/kraft/cap\_levels.py                     |       59 |        0 |    100% |           |
| src/kraft/capabilities.py                    |       38 |        0 |    100% |           |
| src/kraft/caps.py                            |      294 |       16 |     95% |141, 360, 386, 397, 409-410, 423, 520, 592, 630-632, 676-679 |
| src/kraft/cli/\_\_init\_\_.py                |       56 |       12 |     79% |95-101, 134-141, 148 |
| src/kraft/cli/addon.py                       |      504 |       39 |     92% |107-108, 160, 279, 284, 309, 319-320, 332, 383-384, 419-420, 422, 426, 450, 482, 485-486, 546, 553-556, 573-574, 649-650, 687-688, 693, 717-718, 722, 729, 731, 733, 736, 738 |
| src/kraft/cli/admin.py                       |      750 |       43 |     94% |87, 170-172, 190, 196-200, 209, 251, 287-288, 383-384, 392, 406, 521, 642, 669, 799-800, 973-976, 1124-1125, 1243-1244, 1249, 1252, 1261-1267, 1306-1307, 1507, 1534 |
| src/kraft/cli/common.py                      |       41 |        0 |    100% |           |
| src/kraft/cli/item.py                        |      390 |       12 |     97% |32, 107, 159, 162, 194, 272, 424, 447, 484-485, 498, 557 |
| src/kraft/cli/repo.py                        |      371 |       17 |     95% |140, 148, 163, 176-177, 232, 234, 334, 365, 426, 430, 484, 493, 495, 500, 544-545 |
| src/kraft/cli/templates.py                   |       78 |        1 |     99% |       114 |
| src/kraft/cli/verify.py                      |      154 |        5 |     97% |133, 211-214 |
| src/kraft/cli/view.py                        |      301 |       10 |     97% |82, 286-287, 309, 319, 369-370, 406-412 |
| src/kraft/client/\_\_init\_\_.py             |        5 |        0 |    100% |           |
| src/kraft/client/actions.py                  |      222 |       27 |     88% |64, 167, 184, 203, 224, 237, 301, 325-326, 365, 387, 389, 415, 422-426, 504-505, 527, 553, 565, 600, 615, 639, 701 |
| src/kraft/client/context.py                  |       51 |        2 |     96% |     44-45 |
| src/kraft/client/reads.py                    |      178 |        9 |     95% |257-258, 268-275, 374, 380, 426 |
| src/kraft/client/transport.py                |       95 |        9 |     91% |54, 69-70, 87, 177-178, 180, 191-192 |
| src/kraft/config.py                          |      660 |       13 |     98% |105, 128, 185-187, 336, 580, 828, 872-873, 1089-1090, 1177 |
| src/kraft/config\_schemas.py                 |       75 |        7 |     91% |   165-171 |
| src/kraft/db.py                              |      148 |        4 |     97% |1387, 1413-1415 |
| src/kraft/detect.py                          |     1085 |       64 |     94% |202, 357-359, 366-368, 455-462, 483, 578-579, 593, 601, 615, 635, 680, 686, 900, 913, 931, 949, 951, 1012-1013, 1087-1088, 1102, 1178, 1181, 1260, 1272, 1285, 1314-1316, 1326, 1467-1468, 1579, 1669-1670, 1672, 1845-1863, 1950, 2017 |
| src/kraft/doctor.py                          |      749 |       45 |     94% |173, 303-304, 383-384, 438, 442, 460, 464-465, 507, 554, 558, 604-605, 623-624, 712-713, 756-763, 813-814, 893-894, 1036-1037, 1090, 1102-1103, 1252-1253, 1336, 1354, 1367, 1377, 1419, 1427, 1523-1524, 1552, 1556-1557, 1583-1584 |
| src/kraft/drafts/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/drafts/areas.py                    |        6 |        0 |    100% |           |
| src/kraft/drafts/authored.py                 |      239 |       14 |     94% |83, 134, 158, 247, 293, 305, 310, 318, 331-332, 352, 358, 376, 381 |
| src/kraft/drafts/config.py                   |      114 |        9 |     92% |47, 102-103, 121-122, 173-174, 176-177 |
| src/kraft/drafts/harnesses.py                |      324 |       21 |     94% |141, 159, 166, 240, 243, 245, 256, 258, 266, 270-273, 276, 280, 347, 358, 371-372, 442-444 |
| src/kraft/drafts/intake.py                   |      109 |        4 |     96% |46, 109-110, 164 |
| src/kraft/drafts/item.py                     |       88 |        2 |     98% |   88, 118 |
| src/kraft/drafts/ops.py                      |      710 |       72 |     90% |86, 136, 175-176, 197, 204, 209, 215, 221, 227-228, 234-235, 251, 256, 340, 347-348, 403, 453, 455, 484-485, 515, 546, 566, 588, 593-594, 599, 609, 622, 634-639, 651, 676, 706, 714, 720, 740, 754, 767, 771, 774, 801, 806, 852, 877, 895, 912, 929, 931, 935-937, 940, 943, 958, 961, 988, 994-995, 1000, 1002, 1052-1053, 1061-1062 |
| src/kraft/drafts/policy.py                   |      178 |       12 |     93% |58, 72, 89-91, 106, 174, 187-188, 248, 250, 253 |
| src/kraft/drafts/policy\_caps.py             |       60 |        3 |     95% | 43, 49-50 |
| src/kraft/drafts/preserve.py                 |      281 |       22 |     92% |142-143, 178-179, 182, 300-314, 423, 426-427, 469 |
| src/kraft/drafts/repos.py                    |      160 |        7 |     96% |37, 45, 50, 78, 224, 229-230 |
| src/kraft/drafts/resolve.py                  |      430 |       23 |     95% |121, 128-129, 185-186, 208, 214-215, 313-314, 329-330, 360, 378, 467, 488, 635, 643-644, 659, 691, 723-724 |
| src/kraft/drafts/store.py                    |       78 |        0 |    100% |           |
| src/kraft/escalate.py                        |      210 |        6 |     97% |190, 296, 423, 605-616, 666 |
| src/kraft/events.py                          |       31 |        0 |    100% |           |
| src/kraft/executor/\_\_init\_\_.py           |       10 |        0 |    100% |           |
| src/kraft/executor/context.py                |       56 |        2 |     96% |  220, 251 |
| src/kraft/executor/dispatch.py               |      834 |       18 |     98% |272, 341, 363-364, 495, 646, 649, 939-940, 1096-1097, 1330-1331, 1730, 1738, 2445, 2798, 2804 |
| src/kraft/executor/entry.py                  |      153 |        1 |     99% |       398 |
| src/kraft/executor/fallback.py               |       83 |        0 |    100% |           |
| src/kraft/executor/gates.py                  |      325 |       10 |     97% |238, 362, 365, 368, 373, 754, 771, 885-886, 1200 |
| src/kraft/executor/prompts.py                |      204 |        7 |     97% |153-160, 247, 694 |
| src/kraft/executor/read\_only.py             |       75 |        2 |     97% |    69, 82 |
| src/kraft/executor/resuming.py               |       89 |        2 |     98% |  140, 183 |
| src/kraft/executor/retry.py                  |       26 |        0 |    100% |           |
| src/kraft/executor/stops.py                  |      147 |        0 |    100% |           |
| src/kraft/executor/walk.py                   |      624 |       15 |     98% |89-90, 670, 789, 1090, 1117, 1129, 1202-1217, 1262, 1499, 1676, 1831, 1888, 1934 |
| src/kraft/findings.py                        |      112 |        0 |    100% |           |
| src/kraft/gate\_review.py                    |       83 |        4 |     95% |103-106, 111, 200 |
| src/kraft/grants.py                          |       64 |        0 |    100% |           |
| src/kraft/harness.py                         |      335 |       18 |     95% |194, 202, 217, 238, 258, 265, 272, 284, 404, 563, 565, 567, 576, 595-596, 633-635 |
| src/kraft/ids.py                             |       29 |        0 |    100% |           |
| src/kraft/index/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| src/kraft/index/chunk.py                     |       44 |        1 |     98% |        65 |
| src/kraft/index/db.py                        |       68 |        5 |     93% |158-159, 168-170 |
| src/kraft/index/embed.py                     |       63 |       13 |     79% |37-38, 68, 73, 78-84, 104-106 |
| src/kraft/index/ingest.py                    |      262 |        9 |     97% |236-237, 358, 448-450, 560-562 |
| src/kraft/index/service.py                   |      416 |       27 |     94% |141-143, 196, 267-269, 306, 325-327, 380-381, 386, 389-390, 572, 606-607, 623, 641, 645-646, 833, 836, 842, 904 |
| src/kraft/init.py                            |       51 |        2 |     96% |     62-64 |
| src/kraft/intake.py                          |      134 |       12 |     91% |99-101, 117, 160-161, 198-200, 219-224, 260 |
| src/kraft/intent.py                          |      198 |        9 |     95% |91-92, 186, 203, 264-265, 321-322, 339 |
| src/kraft/item\_paths.py                     |      299 |       60 |     80% |109, 112, 366, 394, 412-413, 429-432, 444-460, 470-474, 477-479, 496-511, 518-519, 532, 543-546, 617-618, 640 |
| src/kraft/logs.py                            |      177 |       10 |     94% |103, 108, 125, 135, 152, 168-169, 177-178, 278 |
| src/kraft/mcp.py                             |      148 |        2 |     99% |   581-582 |
| src/kraft/mr\_poller.py                      |       68 |        9 |     87% |72-73, 85-86, 92, 127-130 |
| src/kraft/node\_runs.py                      |       64 |        1 |     98% |        55 |
| src/kraft/notify.py                          |      153 |       10 |     93% |184-185, 269-276, 289-292, 318 |
| src/kraft/overrides.py                       |       98 |        3 |     97% |116, 189-190 |
| src/kraft/paths.py                           |      102 |        0 |    100% |           |
| src/kraft/permission\_hooks.py               |       70 |        1 |     99% |        40 |
| src/kraft/permission\_rules.py               |       40 |        0 |    100% |           |
| src/kraft/pidfile.py                         |      125 |       19 |     85% |51-52, 57-58, 80-81, 117, 134, 145-146, 160-161, 169-170, 172, 196-197, 199-200 |
| src/kraft/policy.py                          |      796 |       24 |     97% |173, 295-296, 602, 607-608, 1282, 1469, 1703-1712, 1792, 1799, 1813, 1817-1821, 1826 |
| src/kraft/progress.py                        |      151 |        0 |    100% |           |
| src/kraft/rate\_limit\_retry.py              |       59 |        7 |     88% |160-162, 172-175 |
| src/kraft/registration.py                    |       59 |        0 |    100% |           |
| src/kraft/render.py                          |      274 |       24 |     91% |59-60, 97, 104, 382, 393, 408, 421, 427-431, 469-476, 527, 539, 565 |
| src/kraft/review.py                          |      183 |        5 |     97% |99, 227, 231, 279, 332 |
| src/kraft/review\_reply.py                   |       81 |        7 |     91% |76, 98-99, 131-132, 137, 159 |
| src/kraft/skill.py                           |       85 |        8 |     91% |83-84, 113, 191, 196-197, 201-202 |
| src/kraft/start\_queue.py                    |       77 |        5 |     94% |105, 170-173 |
| src/kraft/storage.py                         |      256 |       14 |     95% |102-103, 132-133, 168-169, 185-186, 205, 327, 448-451 |
| src/kraft/store/\_\_init\_\_.py              |       13 |        0 |    100% |           |
| src/kraft/store/\_common.py                  |       46 |        2 |     96% |  127, 145 |
| src/kraft/store/budget.py                    |       69 |        0 |    100% |           |
| src/kraft/store/chain.py                     |      203 |        4 |     98% |364, 454-456 |
| src/kraft/store/counters.py                  |       55 |        0 |    100% |           |
| src/kraft/store/forks.py                     |       44 |        0 |    100% |           |
| src/kraft/store/gates.py                     |       52 |        0 |    100% |           |
| src/kraft/store/intake.py                    |       14 |        0 |    100% |           |
| src/kraft/store/passes.py                    |       56 |        0 |    100% |           |
| src/kraft/store/repos.py                     |       19 |        0 |    100% |           |
| src/kraft/store/review.py                    |      181 |        4 |     98% |212, 217, 224-225 |
| src/kraft/store/sessions.py                  |      186 |        0 |    100% |           |
| src/kraft/store/work\_items.py               |      299 |        4 |     99% |385, 420, 601, 608 |
| src/kraft/templates/\_\_init\_\_.py          |        0 |        0 |    100% |           |
| src/kraft/templates/catalogue.py             |       59 |        0 |    100% |           |
| src/kraft/templates/environment.py           |      312 |        4 |     99% |534, 536, 592-593 |
| src/kraft/templates/forks.py                 |      100 |        0 |    100% |           |
| src/kraft/templates/library.py               |      519 |        6 |     99% |262, 269, 409-410, 425, 726 |
| src/kraft/templates/models.py                |      710 |        7 |     99% |109, 112, 566, 744, 1335-1336, 1601 |
| src/kraft/templates/positions.py             |       57 |        0 |    100% |           |
| src/kraft/templates/retry.py                 |      105 |       11 |     90% |191, 193-199, 201-202, 209 |
| src/kraft/templates/revision.py              |      272 |        9 |     97% |218, 263, 317, 433, 519, 565-566, 568, 582 |
| src/kraft/triggers.py                        |       79 |        6 |     92% |107-108, 147-150 |
| src/kraft/update.py                          |      250 |       12 |     95% |80-81, 111-115, 120, 205-208, 363-364 |
| src/kraft/usage.py                           |      485 |       22 |     95% |119-120, 226, 357, 478, 538, 558-559, 562-563, 607, 686, 706-707, 978-979, 1084-1085, 1118-1119, 1269, 1281 |
| src/kraft/vocab/\_\_init\_\_.py              |        7 |        0 |    100% |           |
| src/kraft/vocab/display.py                   |       14 |        0 |    100% |           |
| src/kraft/vocab/events/\_\_init\_\_.py       |       32 |        0 |    100% |           |
| src/kraft/vocab/events/chain.py              |       29 |        0 |    100% |           |
| src/kraft/vocab/events/escalation.py         |       15 |        0 |    100% |           |
| src/kraft/vocab/events/forge.py              |       21 |        0 |    100% |           |
| src/kraft/vocab/events/gate.py               |       26 |        0 |    100% |           |
| src/kraft/vocab/events/limit.py              |       17 |        0 |    100% |           |
| src/kraft/vocab/events/sandbox.py            |       12 |        0 |    100% |           |
| src/kraft/vocab/events/session.py            |       17 |        0 |    100% |           |
| src/kraft/vocab/events/settings.py           |       14 |        0 |    100% |           |
| src/kraft/vocab/events/traits.py             |        8 |        0 |    100% |           |
| src/kraft/vocab/events/work\_item.py         |       35 |        0 |    100% |           |
| src/kraft/vocab/review.py                    |       22 |        0 |    100% |           |
| src/kraft/vocab/session.py                   |       42 |        0 |    100% |           |
| src/kraft/vocab/sql.py                       |       29 |        0 |    100% |           |
| src/kraft/vocab/stop.py                      |       26 |        0 |    100% |           |
| src/kraft/vocab/total.py                     |       11 |        0 |    100% |           |
| src/kraft/vocab/work\_item.py                |       98 |        0 |    100% |           |
| src/kraft/waits.py                           |      106 |        7 |     93% |296-298, 308-311 |
| src/kraft/worker/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| src/kraft/worker/backends/\_\_init\_\_.py    |       35 |        0 |    100% |           |
| src/kraft/worker/backends/docker.py          |      818 |       55 |     93% |348, 360-363, 375-382, 459, 574, 622, 631-632, 650, 680, 705-706, 733, 736-739, 808, 1021-1022, 1142-1143, 1170, 1316-1317, 1367, 1459-1462, 1555-1556, 1581-1582, 1625, 1689-1690, 1734, 1762, 1820-1821, 1860-1861, 1954-1955, 1981-1982 |
| src/kraft/worker/backends/docker\_forward.py |      136 |        7 |     95% |92-93, 95, 214-216, 224 |
| src/kraft/worker/ca.py                       |      108 |        1 |     99% |       306 |
| src/kraft/worker/callback.py                 |       37 |        1 |     97% |        43 |
| src/kraft/worker/channel.py                  |      168 |        7 |     96% |161, 169, 203-204, 305, 331-332 |
| src/kraft/worker/egress.py                   |      470 |       36 |     92% |286-287, 293, 334-336, 355, 391, 397, 413-414, 424, 442, 444, 504, 559, 567-568, 675, 686, 709, 725, 749-750, 752-753, 765, 768, 798-799, 849-854 |
| src/kraft/worker/env.py                      |       11 |        0 |    100% |           |
| src/kraft/worker/inject.py                   |      238 |       18 |     92% |194, 214, 230, 241, 253, 351, 365, 374, 384, 390, 393, 407, 410, 415, 424-427 |
| src/kraft/worker/kit.py                      |      421 |       10 |     98% |124, 238-240, 430, 669-670, 672, 698, 732 |
| src/kraft/worker/reattach.py                 |      315 |       26 |     92% |112-113, 122-123, 131-132, 165-166, 278, 324, 336-337, 368, 441, 449, 463-464, 642, 652-653, 729-733, 746-747, 764-765 |
| src/kraft/worker/refstore.py                 |      224 |        7 |     97% |187, 190, 306, 394-395, 423, 446 |
| src/kraft/worker/sandbox.py                  |      158 |        7 |     96% |110, 148-149, 154-155, 192, 217 |
| src/kraft/worker/session\_mcp.py             |       23 |        4 |     83% |45, 50-51, 53 |
| src/kraft/worker/shim.py                     |        4 |        0 |    100% |           |
| src/kraft/worker/steering.py                 |       37 |        0 |    100% |           |
| src/kraft/worker/tree\_walk.py               |       99 |       12 |     88% |71-72, 132-133, 135-136, 171-172, 181-182, 185-186 |
| src/kraft/worker/worktree\_read.py           |       90 |        8 |     91% |52, 165-167, 170-174, 182-183 |
| src/kraft/ws.py                              |       72 |        3 |     96% |     77-79 |
| **TOTAL**                                    | **36889** | **1747** | **95%** |           |


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