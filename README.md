# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Aarhus-Psychiatry-Research/psycop-common/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                                                                  |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------------------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/\_\_init\_\_.py                                                                                                   |        0 |        0 |    100% |           |
| src/psycop/\_\_init\_\_.py                                                                                            |        0 |        0 |    100% |           |
| src/psycop/common/feature\_generation/\_\_init\_\_.py                                                                 |        0 |        0 |    100% |           |
| src/psycop/common/feature\_generation/application\_modules/\_\_init\_\_.py                                            |        0 |        0 |    100% |           |
| src/psycop/common/feature\_generation/application\_modules/filter\_prediction\_times.py                               |       42 |        5 |     88% |43, 61-63, 79, 140 |
| src/psycop/common/feature\_generation/application\_modules/project\_setup.py                                          |       47 |       18 |     62% |45-50, 69-73, 86-97, 115-132 |
| src/psycop/common/feature\_generation/application\_modules/save\_dataset\_to\_disk.py                                 |       31 |       17 |     45% |26-35, 45-57, 62-66, 80-89 |
| src/psycop/common/feature\_generation/application\_modules/wandb\_utils.py                                            |       10 |        5 |     50% |     11-15 |
| src/psycop/common/feature\_generation/data\_checks/\_\_init\_\_.py                                                    |        0 |        0 |    100% |           |
| src/psycop/common/feature\_generation/data\_checks/flattened/feature\_describer.py                                    |       74 |       20 |     73% |58-60, 78-93, 103, 169, 192-203, 247 |
| src/psycop/common/feature\_generation/data\_checks/raw/check\_raw\_df.py                                              |       62 |        8 |     87% |84, 168-173, 183, 214 |
| src/psycop/common/feature\_generation/data\_checks/utils.py                                                           |       14 |        1 |     93% |        69 |
| src/psycop/common/feature\_generation/loaders/\_\_init\_\_.py                                                         |        0 |        0 |    100% |           |
| src/psycop/common/feature\_generation/loaders/filters/\_\_init\_\_.py                                                 |        0 |        0 |    100% |           |
| src/psycop/common/feature\_generation/loaders/filters/diabetes\_filters.py                                            |       12 |        3 |     75% |     38-45 |
| src/psycop/common/feature\_generation/loaders/flattened/\_\_init\_\_.py                                               |        1 |        0 |    100% |           |
| src/psycop/common/feature\_generation/loaders/flattened/local\_feature\_loaders.py                                    |       16 |        5 |     69% |23-26, 72, 94, 114 |
| src/psycop/common/feature\_generation/loaders/non\_numerical\_coercer.py                                              |       13 |        0 |    100% |           |
| src/psycop/common/feature\_generation/loaders/raw/\_\_init\_\_.py                                                     |       10 |        0 |    100% |           |
| src/psycop/common/feature\_generation/loaders/raw/load\_coercion.py                                                   |      102 |       52 |     49% |32-74, 96-117, 126-135, 150, 165, 179, 193, 207, 223-232, 247-262, 276-288, 303-323, 341, 355, 369, 383, 397, 411, 425, 439, 453, 467, 481 |
| src/psycop/common/feature\_generation/loaders/raw/load\_demographic.py                                                |       21 |       13 |     38% |12-24, 29-42 |
| src/psycop/common/feature\_generation/loaders/raw/load\_diagnoses.py                                                  |      196 |       73 |     63% |53-96, 107, 126, 148, 167, 186, 205, 224, 243-272, 283-312, 325, 344, 363, 382, 402, 421, 440, 459, 478, 497, 516, 535, 554, 576, 595, 614, 633, 655, 674, 693, 712, 734, 753, 772, 791, 813, 832, 851, 870, 890, 909, 928, 947, 966, 985, 1007, 1026, 1045, 1064, 1083, 1103, 1122, 1141, 1161, 1180, 1199, 1218, 1238 |
| src/psycop/common/feature\_generation/loaders/raw/load\_ids.py                                                        |        8 |        4 |     50% |     19-25 |
| src/psycop/common/feature\_generation/loaders/raw/load\_lab\_results.py                                               |      180 |       92 |     49% |30-53, 72-94, 112-138, 156-179, 197-237, 248, 260-307, 319, 331, 343-350, 362, 374, 386, 398, 410, 422, 434, 446, 458, 470, 482, 494, 506, 518, 530, 542, 554, 566, 578, 590, 602, 614, 626, 638, 650, 662, 674, 686, 698, 710, 722, 734, 746, 761 |
| src/psycop/common/feature\_generation/loaders/raw/load\_medications.py                                                |      186 |       72 |     61% |52-112, 134-143, 167, 188, 216, 253, 277, 301, 324, 347, 376, 402, 426, 452, 471, 490, 509, 528, 547, 567, 588, 608, 629, 648, 667, 687, 707, 727, 746, 765, 784, 803, 822, 841, 860, 880, 900, 919, 938, 957, 976, 995, 1014, 1033, 1052, 1071, 1090, 1109, 1128, 1147, 1166, 1185, 1204, 1223, 1243 |
| src/psycop/common/feature\_generation/loaders/raw/load\_structured\_sfi.py                                            |       48 |       27 |     44% |28-55, 60, 72-88, 93-110, 115, 125, 135, 145-154, 159-168 |
| src/psycop/common/feature\_generation/loaders/raw/load\_t2d\_outcomes.py                                              |       19 |       11 |     42% |12-23, 28-41 |
| src/psycop/common/feature\_generation/loaders/raw/load\_text.py                                                       |       52 |       31 |     40% |27, 72-82, 108-141, 162-178, 193, 211, 232, 257-269 |
| src/psycop/common/feature\_generation/loaders/raw/load\_visits.py                                                     |       70 |       41 |     41% |63-167, 176, 190-201, 210, 226, 243, 260, 277 |
| src/psycop/common/feature\_generation/loaders/raw/sql\_load.py                                                        |       21 |       13 |     38% |     41-69 |
| src/psycop/common/feature\_generation/loaders/raw/utils.py                                                            |       70 |       51 |     27% |26-37, 54-76, 132-282 |
| src/psycop/common/feature\_generation/text\_models/fit\_text\_models.py                                               |       10 |        1 |     90% |        34 |
| src/psycop/common/feature\_generation/text\_models/preprocessing.py                                                   |       21 |        5 |     76% |     69-89 |
| src/psycop/common/feature\_generation/text\_models/test\_text\_models/test\_models.py                                 |       18 |        0 |    100% |           |
| src/psycop/common/feature\_generation/text\_models/test\_text\_models/test\_preprocessing.py                          |        7 |        0 |    100% |           |
| src/psycop/common/feature\_generation/text\_models/utils.py                                                           |       12 |        5 |     58% |22-23, 36-40 |
| src/psycop/common/feature\_generation/utils.py                                                                        |       45 |       26 |     42% |35, 62, 66, 70, 91-98, 111, 125-132, 142-157 |
| src/psycop/common/global\_utils/cache.py                                                                              |        8 |        1 |     88% |         8 |
| src/psycop/common/global\_utils/paths.py                                                                              |        4 |        0 |    100% |           |
| src/psycop/common/global\_utils/pickle.py                                                                             |       11 |        6 |     45% |7-10, 14-17 |
| src/psycop/common/model\_evaluation/\_\_init\_\_.py                                                                   |        0 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/bootstrap\_estimates.py                                                    |       18 |        3 |     83% |     35-37 |
| src/psycop/common/model\_evaluation/binary/global\_performance/roc\_auc.py                                            |       33 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/global\_performance/test\_global\_performance\_plots.py                    |        6 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/performance\_by\_ppr/performance\_by\_ppr.py                               |       55 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/performance\_by\_ppr/prop\_of\_all\_events\_hit\_by\_true\_positive.py     |        9 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/performance\_by\_ppr/test\_performance\_by\_ppr.py                         |       13 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/subgroup\_data.py                                                          |       15 |        1 |     93% |        46 |
| src/psycop/common/model\_evaluation/binary/test\_bootstrap\_estimates.py                                              |        9 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/test\_subgroup\_data.py                                                    |       20 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/time/absolute\_data.py                                                     |        8 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/time/test\_absolute\_data.py                                               |       12 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/time/test\_timedelta\_data.py                                              |       13 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/binary/time/timedelta\_data.py                                                    |       37 |        6 |     84% |38, 105, 148-170 |
| src/psycop/common/model\_evaluation/binary/utils.py                                                                   |       35 |        6 |     83% |20, 65, 109-115 |
| src/psycop/common/model\_evaluation/confusion\_matrix/confusion\_matrix.py                                            |       27 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/confusion\_matrix/test\_confusion\_matrix.py                                      |       13 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/patchwork/patchwork\_grid.py                                                      |       35 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/patchwork/test\_patchwork\_grid.py                                                |       12 |        0 |    100% |           |
| src/psycop/common/model\_evaluation/utils.py                                                                          |      107 |       46 |     57% |61, 90-101, 121, 137-140, 168, 185, 194, 239-245, 257-258, 272-279, 291, 309-312, 319-324, 332-343, 348, 356-363 |
| src/psycop/common/model\_training/\_\_init\_\_.py                                                                     |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/application\_modules/\_\_init\_\_.py                                                |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/application\_modules/train\_model/\_\_init\_\_.py                                   |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/application\_modules/train\_model/main.py                                           |       38 |        1 |     97% |        39 |
| src/psycop/common/model\_training/application\_modules/wandb\_handler.py                                              |       34 |        2 |     94% |    46, 68 |
| src/psycop/common/model\_training/config\_schemas/\_\_init\_\_.py                                                     |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/basemodel.py                                                        |       18 |        1 |     94% |        25 |
| src/psycop/common/model\_training/config\_schemas/conf\_utils.py                                                      |       29 |        2 |     93% |     65-71 |
| src/psycop/common/model\_training/config\_schemas/data.py                                                             |       22 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/debug.py                                                            |        5 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/full\_config.py                                                     |       15 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/model.py                                                            |        5 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/preprocessing.py                                                    |       27 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/project.py                                                          |       10 |        0 |    100% |           |
| src/psycop/common/model\_training/config\_schemas/train.py                                                            |        5 |        0 |    100% |           |
| src/psycop/common/model\_training/data\_loader/\_\_init\_\_.py                                                        |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/data\_loader/col\_name\_checker.py                                                  |       29 |        0 |    100% |           |
| src/psycop/common/model\_training/data\_loader/data\_loader.py                                                        |       43 |       11 |     74% |42, 64, 69-74, 78, 102-110 |
| src/psycop/common/model\_training/data\_loader/utils.py                                                               |       32 |       14 |     56% | 22, 79-96 |
| src/psycop/common/model\_training/preprocessing/\_\_init\_\_.py                                                       |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/preprocessing/post\_split/\_\_init\_\_.py                                           |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/preprocessing/post\_split/create\_pipeline.py                                       |       31 |        5 |     84% |21, 59, 76-80, 114 |
| src/psycop/common/model\_training/preprocessing/post\_split/pipeline.py                                               |       15 |        0 |    100% |           |
| src/psycop/common/model\_training/preprocessing/pre\_split/\_\_init\_\_.py                                            |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/preprocessing/pre\_split/full\_processor.py                                         |       34 |        0 |    100% |           |
| src/psycop/common/model\_training/preprocessing/pre\_split/processors/col\_filter.py                                  |       86 |       15 |     83% |47, 65-76, 145, 174-182, 201, 212-214 |
| src/psycop/common/model\_training/preprocessing/pre\_split/processors/row\_filter.py                                  |       81 |        7 |     91% |48, 84, 117, 157-159, 170, 177 |
| src/psycop/common/model\_training/preprocessing/pre\_split/processors/value\_cleaner.py                               |       45 |        1 |     98% |       106 |
| src/psycop/common/model\_training/preprocessing/pre\_split/processors/value\_transformer.py                           |       39 |       13 |     67% |39, 45-55, 64-75, 83, 86 |
| src/psycop/common/model\_training/tests/\_\_init\_\_.py                                                               |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/application\_modules/test\_model\_evaluator.py                                |       12 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/application\_modules/test\_train\_model.py                                    |       38 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/application\_modules/test\_wandb\_handler.py                                  |       10 |        2 |     80% |    18, 20 |
| src/psycop/common/model\_training/tests/test\_application\_modules/test\_filter\_prediction\_times.py                 |       10 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_check\_raw\_df/test\_check\_raw\_df.py                                  |       33 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_configs.py                                                              |       19 |        5 |     74% |27-32, 37-39 |
| src/psycop/common/model\_training/tests/test\_data/\_\_init\_\_.py                                                    |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_data/test\_generate\_synth\_splits.py                                   |       19 |        2 |     89% |   108-113 |
| src/psycop/common/model\_training/tests/test\_data/test\_hf/test\_hf\_embeddings.py                                   |        2 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_data/test\_tfidf/test\_tfidf\_vocab.py                                  |        9 |        4 |     56% |     23-28 |
| src/psycop/common/model\_training/tests/test\_feature\_describer/test\_feature\_describer.py                          |       44 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_load.py                                                                 |       23 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_loaders/test\_filters.py                                                |        6 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_loaders/test\_non\_numerical\_coercion.py                               |       11 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_loaders/test\_unpack\_intervals.py                                      |       19 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_performance\_by\_threshold.py                                           |       32 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_preprocessing/test\_row\_filter.py                                      |       33 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_preprocessing/test\_value\_cleaner.py                                   |        8 |        0 |    100% |           |
| src/psycop/common/model\_training/tests/test\_utils.py                                                                |       39 |        1 |     97% |        39 |
| src/psycop/common/model\_training/training/\_\_init\_\_.py                                                            |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/training/model\_specs.py                                                            |       13 |        0 |    100% |           |
| src/psycop/common/model\_training/training/train\_and\_predict.py                                                     |       62 |        0 |    100% |           |
| src/psycop/common/model\_training/training/utils.py                                                                   |       13 |        2 |     85% |    20, 30 |
| src/psycop/common/model\_training/training\_output/\_\_init\_\_.py                                                    |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/training\_output/artifact\_saver/to\_disk.py                                        |       51 |        1 |     98% |        57 |
| src/psycop/common/model\_training/training\_output/dataclasses.py                                                     |       36 |        0 |    100% |           |
| src/psycop/common/model\_training/training\_output/model\_evaluator.py                                                |       32 |        1 |     97% |        39 |
| src/psycop/common/model\_training/training\_output/test\_dataclasses.py                                               |       13 |        0 |    100% |           |
| src/psycop/common/model\_training/utils/\_\_init\_\_.py                                                               |        0 |        0 |    100% |           |
| src/psycop/common/model\_training/utils/col\_name\_inference.py                                                       |       39 |        9 |     77% |33, 62-63, 71, 91-96, 123 |
| src/psycop/common/model\_training/utils/decorators.py                                                                 |       43 |        1 |     98% |        31 |
| src/psycop/common/model\_training/utils/utils.py                                                                      |       95 |       31 |     67% |46, 122-125, 151, 156-157, 165, 170, 174, 219-225, 237-238, 255, 259, 289-292, 300-304, 312-323, 335-339 |
| src/psycop/common/test\_utils/str\_to\_df.py                                                                          |       31 |        1 |     97% |        75 |
| src/psycop/common/test\_utils/test\_data/model\_eval/generate\_synthetic\_dataset\_for\_eval.py                       |       55 |       39 |     29% |37, 42, 61-65, 84-88, 92-170 |
| src/psycop/conftest.py                                                                                                |       47 |        3 |     94% |32, 36, 103 |
| src/psycop/projects/forced\_admission\_inpatient/utils/feature\_name\_to\_readable.py                                 |       26 |        5 |     81% | 15, 39-42 |
| src/psycop/projects/forced\_admission\_inpatient/utils/test\_forced\_admission\_feature\_name\_to\_readable.py        |        7 |        1 |     86% |        15 |
| src/psycop/projects/t2d/paper\_outputs/aggregate\_eval/md\_objects.py                                                 |       53 |        5 |     91% |44, 76-81, 119 |
| src/psycop/projects/t2d/paper\_outputs/aggregate\_eval/test\_md\_objects.py                                           |       38 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/config.py                                                                      |       18 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/conftest.py                        |        7 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/get\_shap\_values.py               |       59 |       33 |     44% |17-28, 33-45, 61, 69-83, 92-124, 152-160 |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/plot\_shap.py                      |       31 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/shap\_table.py                     |        7 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/test\_get\_shap\_values.py         |        6 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/test\_shap\_plot.py                |       13 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/feature\_importance/shap/test\_shap\_table.py               |        9 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/performance/performance\_by\_ppr.py                         |       31 |        7 |     77% |71-83, 87-89 |
| src/psycop/projects/t2d/paper\_outputs/model\_description/performance/plotnine\_confusion\_matrix.py                  |       12 |        1 |     92% |        24 |
| src/psycop/projects/t2d/paper\_outputs/model\_description/performance/sensitivity\_by\_time\_to\_event\_pipeline.py   |       33 |       18 |     45% |47-55, 59-84, 88-94, 98-100 |
| src/psycop/projects/t2d/paper\_outputs/model\_description/performance/test\_plot\_sensitivity\_by\_time\_to\_event.py |       12 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/performance/test\_plotnine\_confusion\_matrix.py            |        7 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/performance/test\_t2d\_performance\_by\_ppr.py              |        9 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_description/robustness/robustness\_plot.py                              |       12 |        1 |     92% |        50 |
| src/psycop/projects/t2d/paper\_outputs/model\_description/robustness/test\_robustness\_plots.py                       |        7 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_permutation/boolean\_features.py                                        |       27 |       12 |     56% |31, 41-59, 63-67 |
| src/psycop/projects/t2d/paper\_outputs/model\_permutation/modified\_dataset.py                                        |       40 |       26 |     35% |17, 28, 35-42, 50-93 |
| src/psycop/projects/t2d/paper\_outputs/model\_permutation/only\_hba1c.py                                              |       41 |       19 |     54% |34-52, 87-112 |
| src/psycop/projects/t2d/paper\_outputs/model\_permutation/test\_boolean\_features.py                                  |       10 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/model\_permutation/test\_only\_hba1c.py                                        |        7 |        0 |    100% |           |
| src/psycop/projects/t2d/paper\_outputs/utils/test\_plotnine\_theme.py                                                 |       10 |        0 |    100% |           |
| src/psycop/projects/t2d/utils/feature\_name\_to\_readable.py                                                          |       26 |        5 |     81% | 15, 44-47 |
| src/psycop/projects/t2d/utils/pipeline\_objects.py                                                                    |      108 |       51 |     53% |20-21, 29, 51, 55-63, 67-73, 76-78, 95-96, 99-103, 106, 109, 116, 129-133, 136-138, 142, 154-161, 174-181, 196-206, 217 |
| src/psycop/projects/t2d/utils/test\_feature\_name\_to\_readable.py                                                    |        7 |        1 |     86% |        13 |
|                                                                                                             **TOTAL** | **4131** | **1027** | **75%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Aarhus-Psychiatry-Research/psycop-common/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Aarhus-Psychiatry-Research/psycop-common/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Aarhus-Psychiatry-Research/psycop-common/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Aarhus-Psychiatry-Research/psycop-common/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FAarhus-Psychiatry-Research%2Fpsycop-common%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Aarhus-Psychiatry-Research/psycop-common/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.