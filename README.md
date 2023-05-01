# PSYCOP

<!-- [![PyPI](https://img.shields.io/pypi/v/psycop-common.svg)][pypi status] -->
<!-- [![Python Version](https://img.shields.io/pypi/pyversions/psycop-common)][pypi status] -->
[![Tests](https://github.com/Aarhus-Psychiatry-Research/psycop-common/actions/workflows/tests.yml/badge.svg)][tests]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/psycop-common/
[tests]: https://github.com/Aarhus-Psychiatry-Research/psycop-common/actions?workflow=Tests
[black]: https://github.com/psf/black


<!-- start short-description -->

The shared code across the PSYCOP projects.

<!-- end short-description -->

## Installation

We recommend installing straight into your `src` folder, so you can make modifications to the libraries when required:

```bash
pip install --src ./src -e git+https://github.com/Aarhus-Psychiatry-Research/psycop-common#egg=psycop
```

## Migrating from the polyrepos
Replace:
`psycop_feature_generation.` -> `psycop.feature_generation.`
`psycop_model_training.` -> `psycop.model_training.`
`psycop_model_evaluation.` -> `psycop.model_evaluation.`

<!--
To see more examples, see the [documentation].

# 📖 Documentation

| Documentation         |                                                          |
| --------------------- | -------------------------------------------------------- |
| 🔧 **[Installation]**  | Installation instructions on how to install this package |
| 📖 **[Documentation]** | A minimal and developing documentation                   |
| 👩‍💻 **[Tutorials]**     | Tutorials for using this package                         |
| 🎛️ **[API Reference]** | API reference for this package                           |
| 📚 **[FAQ]**           | Frequently asked questions                               |


# 💬 Where to ask questions

| Type                           |                        |
| ------------------------------ | ---------------------- |
| 📚 **FAQ**                      | [FAQ]                  |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |

[Documentation]: https://Aarhus-Psychiatry-Research.github.io/psycop-common/index.html
[Installation]: https://Aarhus-Psychiatry-Research.github.io/psycop-common/installation.html
[Tutorials]: https://Aarhus-Psychiatry-Research.github.io/psycop-common/tutorials.html
[API Reference]: https://Aarhus-Psychiatry-Research.github.io/psycop-common/references.html
[FAQ]: https://Aarhus-Psychiatry-Research.github.io/psycop-common/faq.html
[github issue tracker]: https://github.com/Aarhus-Psychiatry-Research/psycop-common/issues
[github discussions]: https://github.com/Aarhus-Psychiatry-Research/psycop-common/discussions
-->
