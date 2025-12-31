./->docker build D:/thebug/TheDev/app/yly/zb/task/sqlmesh/4323 -t sqlmesh:3.9_default
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 1.65kB done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/ubuntu:22.04
#2 DONE 0.6s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [ 1/10] FROM docker.io/library/ubuntu:22.04@sha256:104ae83764a5119017b8e8d6218fa0832b09df65aae7d5a6de29a85d813da2fb
#4 resolve docker.io/library/ubuntu:22.04@sha256:104ae83764a5119017b8e8d6218fa0832b09df65aae7d5a6de29a85d813da2fb 0.0s done
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 1.07kB done
#5 DONE 0.0s

#6 [ 5/10] COPY setup_repo.sh /root/setup_repo.sh
#6 CACHED

#7 [ 2/10] RUN apt-get update && apt-get install -y --no-install-recommends     wget     git     ca-certificates     curl     vim     dos2unix     python3     python3-pip     python-is-python3
#7 CACHED

#8 [ 3/10] RUN wget 'https://repo.anaconda.com/miniconda/Miniconda3-py311_23.11.0-2-Linux-x86_64.sh' -O miniconda.sh &&     bash miniconda.sh -b -p /opt/miniconda3 &&     rm -f miniconda.sh
#8 CACHED

#9 [ 4/10] RUN conda init bash &&     conda config --add channels conda-forge &&     conda config --remove channels defaults
#9 CACHED

#10 [ 6/10] RUN chmod +x /root/setup_repo.sh &&     /bin/bash /root/setup_repo.sh
#10 CACHED

#11 [ 7/10] COPY setup_env.sh /root/setup_env.sh
#11 DONE 0.1s

#12 [ 8/10] RUN chmod +x /root/setup_env.sh &&     /bin/bash -c "source /root/.bashrc && /root/setup_env.sh"
#12 1.413 HEAD is now at ab6bc178 Observability doc drafts (#3515)
#12 2.525 Python 3.9.23
#12 2.525 
#12 3.408 Writing to /root/.config/pip/pip.conf
#12 3.408 
#12 4.721 Writing to /root/.config/pip/pip.conf
#12 4.721 
#12 60.23   DEPRECATION: Legacy editable install of sqlmesh==0.147.1.dev1 from file:///testbed/TobikoData/sqlmesh (setup.py develop) is deprecated. pip 25.3 will enforce this behaviour change. A possible replacement is to add a pyproject.toml or enable --use-pep517, and use setuptools >= 64. If the resulting installation is not behaving as expected, try using --config-settings editable_mode=compat. Please consult the setuptools documentation for more information. Discussion can be found at https://github.com/pypa/pip/issues/11457
#12 60.23 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#12 60.23 
#12 60.23 Looking in indexes: http://mirrors.tools.huawei.com/pypi/simple/
#12 60.23 Obtaining file:///testbed/TobikoData/sqlmesh
#12 60.23   Preparing metadata (setup.py): started
#12 60.23   Preparing metadata (setup.py): finished with status 'done'
#12 60.23 Collecting astor (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c3/88/97eef84f48fa04fbd6750e62dcceafba6c63c81b7ac1420856c8dcc0a3f9/astor-0.8.1-py2.py3-none-any.whl (27 kB)
#12 60.23 Collecting click (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/7e/d4/7ebdbd03970677812aac39c869717059dbb71a4cfc033ca6e5221787892c/click-8.1.8-py3-none-any.whl (98 kB)
#12 60.23 Collecting croniter (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/07/4b/290b4c3efd6417a8b0c284896de19b1d5855e6dbdb97d2a35e68fa42de85/croniter-6.0.0-py2.py3-none-any.whl (25 kB)
#12 60.23 Collecting duckdb!=0.10.3 (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/ec/bc/ed0cf343519ef6a204eeb77e73b851bf92daf35815120402d724a7909231/duckdb-1.4.3-cp39-cp39-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl (20.5 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.5/20.5 MB 8.2 MB/s  0:00:02
#12 60.23 Collecting dateparser (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/87/22/f020c047ae1346613db9322638186468238bcfa8849b4668a22b97faad65/dateparser-1.2.2-py3-none-any.whl (315 kB)
#12 60.23 Collecting hyperscript>=0.1.0 (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/d4/2d/05a668e7dd7eaf0d7ee9bc162ebf358e9be9af43e4720cdecf622ccc6c9b/hyperscript-0.3.0-py3-none-any.whl (5.0 kB)
#12 60.23 Collecting ipywidgets (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/56/6d/0d9848617b9f753b87f214f1c682592f7ca42de085f564352f10f0843026/ipywidgets-8.1.8-py3-none-any.whl (139 kB)
#12 60.23 Collecting jinja2 (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/62/a1/3d680cbfd5f4b8f15abc1d571870c5fc3e594bb582bc3b64ea099db13e56/jinja2-3.1.6-py3-none-any.whl (134 kB)
#12 60.23 Collecting pandas (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/1f/18/aae8c0aa69a386a3255940e9317f793808ea79d0a525a97a903366bb2569/pandas-2.3.3-cp39-cp39-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.8 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 6.0 MB/s  0:00:02
#12 60.23 Collecting pydantic>=2.0.0 (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/5a/87/b70ad306ebb6f9b585f114d0ac2137d792b48be34d732d60e597c2f8465a/pydantic-2.12.5-py3-none-any.whl (463 kB)
#12 60.23 Collecting requests (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl (64 kB)
#12 60.23 Collecting rich[jupyter] (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/25/7a/b0178788f8dc6cafce37a212c99565fa1fe7872c70c6c9c1e1a372d9d88f/rich-14.2.0-py3-none-any.whl (243 kB)
#12 60.23 Collecting ruamel.yaml (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/af/fe/b6045c782f1fd1ae317d2a6ca1884857ce5c20f59befe6ab25a8603c43a7/ruamel_yaml-0.18.17-py3-none-any.whl (121 kB)
#12 60.23 Collecting sqlglot~=26.2.1 (from sqlglot[rs]~=26.2.1->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/ed/50/4aca824214afea433d9827afc4f4f9640ab50b7d0ac45a5aee286193469a/sqlglot-26.2.1-py3-none-any.whl (443 kB)
#12 60.23 Collecting tenacity (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/e5/30/643397144bfbfec6f6ef821f36f33e57d35946c44a2352d3c9f0ae847619/tenacity-9.1.2-py3-none-any.whl (28 kB)
#12 60.23 Collecting time-machine (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/94/b0/8ef58e2f6321851d5900ca3d18044938832c2ed42a2ac7570ca6aa29768a/time_machine-2.19.0-cp39-cp39-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (34 kB)
#12 60.23 Collecting importlib-metadata (from sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/fa/5e/f8e9a1d23b9c20a551a8a02ea3637b4642e22c2626e3a13a9a29cdea99eb/importlib_metadata-8.7.1-py3-none-any.whl (27 kB)
#12 60.23 Collecting sqlglotrs==0.3.5 (from sqlglot[rs]~=26.2.1->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/e8/c0/fc358c1b9e4e761652b1045d1b3be1823ea5b88b7eca5d29fbda92882d11/sqlglotrs-0.3.5-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (332 kB)
#12 60.23 Collecting annotated-types>=0.6.0 (from pydantic>=2.0.0->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/78/b6/6307fbef88d9b5ee7421e68d78a9f162e0da4900bc5f5793f6d3d0e34fb8/annotated_types-0.7.0-py3-none-any.whl (13 kB)
#12 60.23 Collecting pydantic-core==2.41.5 (from pydantic>=2.0.0->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c0/4a/412d2048be12c334003e9b823a3fa3d038e46cc2d64dd8aab50b31b65499/pydantic_core-2.41.5-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 11.0 MB/s  0:00:00
#12 60.23 Collecting typing-extensions>=4.14.1 (from pydantic>=2.0.0->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/18/67/36e9267722cc04a6b9f15c7f3441c2363321a3ea07da7ae0c0707beb2a9c/typing_extensions-4.15.0-py3-none-any.whl (44 kB)
#12 60.23 Collecting typing-inspection>=0.4.2 (from pydantic>=2.0.0->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/dc/9b/47798a6c91d8bdb567fe2698fe81e0c6b7cb7ef4d13da4114b41d239f65d/typing_inspection-0.4.2-py3-none-any.whl (14 kB)
#12 60.23 Collecting python-dateutil (from croniter->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/ec/57/56b9bcc3c9c6a792fcbaf139543cee77261f3651ca9da0c93f5c1221264b/python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
#12 60.23 Collecting pytz>2021.1 (from croniter->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/81/c4/34e93fe5f5429d7570ec1fa436f1986fb1f00c3e0f43a589fe2bbcd22c3f/pytz-2025.2-py2.py3-none-any.whl (509 kB)
#12 60.23 Collecting regex>=2024.9.11 (from dateparser->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/60/ee/e9c71bdf334edc14ff769463bd6173966b0445e442a28b18f790b84032f5/regex-2025.11.3-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (791 kB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 791.2/791.2 kB 8.0 MB/s  0:00:00
#12 60.23 Collecting tzlocal>=0.2 (from dateparser->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c2/14/e2a54fabd4f08cd7af1c07030603c3356b74da07f7cc056e600436edfa17/tzlocal-5.3.1-py3-none-any.whl (18 kB)
#12 60.23 Collecting six>=1.5 (from python-dateutil->croniter->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/b7/ce/149a00dd41f10bc29e5921b496af8b574d8413afcd5e30dfa0ed46c2cc5e/six-1.17.0-py2.py3-none-any.whl (11 kB)
#12 60.23 Collecting zipp>=3.20 (from importlib-metadata->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/2e/54/647ade08bf0db230bfea292f893923872fd20be6ac6f53b2b936ba839d75/zipp-3.23.0-py3-none-any.whl (10 kB)
#12 60.23 Collecting comm>=0.1.3 (from ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/60/97/891a0971e1e4a8c5d2b20bbe0e524dc04548d2307fee33cdeba148fd4fc7/comm-0.2.3-py3-none-any.whl (7.3 kB)
#12 60.23 Collecting ipython>=6.1.0 (from ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/47/6b/d9fdcdef2eb6a23f391251fde8781c38d42acd82abe84d054cb74f7863b0/ipython-8.18.1-py3-none-any.whl (808 kB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 808.2/808.2 kB 8.1 MB/s  0:00:00
#12 60.23 Collecting traitlets>=4.3.1 (from ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/00/c0/8f5d070730d7836adc9c9b6408dec68c6ced86b304a9b26a14df072a6e8c/traitlets-5.14.3-py3-none-any.whl (85 kB)
#12 60.23 Collecting widgetsnbextension~=4.0.14 (from ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/3f/0e/fa3b193432cfc60c93b42f3be03365f5f909d2b3ea410295cf36df739e31/widgetsnbextension-4.0.15-py3-none-any.whl (2.2 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.2/2.2 MB 13.2 MB/s  0:00:00
#12 60.23 Collecting jupyterlab_widgets~=3.0.15 (from ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/ab/b5/36c712098e6191d1b4e349304ef73a8d06aed77e56ceaac8c0a306c7bda1/jupyterlab_widgets-3.0.16-py3-none-any.whl (914 kB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 914.9/914.9 kB 7.3 MB/s  0:00:00
#12 60.23 Collecting decorator (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/4e/8c/f3147f5c4b73e7550fe5f9352eaa956ae838d5c51eb58e7a25b9f3e2643b/decorator-5.2.1-py3-none-any.whl (9.2 kB)
#12 60.23 Collecting jedi>=0.16 (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c0/5a/9cac0c82afec3d09ccd97c8b6502d48f165f9124db81b4bcb90b4af974ee/jedi-0.19.2-py2.py3-none-any.whl (1.6 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 9.3 MB/s  0:00:00
#12 60.23 Collecting matplotlib-inline (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/af/33/ee4519fa02ed11a94aef9559552f3b17bb863f2ecfe1a35dc7f548cde231/matplotlib_inline-0.2.1-py3-none-any.whl (9.5 kB)
#12 60.23 Collecting prompt-toolkit<3.1.0,>=3.0.41 (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/84/03/0d3ce49e2505ae70cf43bc5bb3033955d2fc9f932163e84dc0779cc47f48/prompt_toolkit-3.0.52-py3-none-any.whl (391 kB)
#12 60.23 Collecting pygments>=2.4.0 (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c7/21/705964c7812476f378728bdf590ca4b771ec72385c533964653c68e86bdc/pygments-2.19.2-py3-none-any.whl (1.2 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 8.1 MB/s  0:00:00
#12 60.23 Collecting stack-data (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/f1/7b/ce1eafaf1a76852e2ec9b22edecf1daa58175c090266e9f6c64afcd81d91/stack_data-0.6.3-py3-none-any.whl (24 kB)
#12 60.23 Collecting exceptiongroup (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/8a/0e/97c33bf5009bdbac74fd2beace167cab3f978feb69cc36f1ef79360d6c4e/exceptiongroup-1.3.1-py3-none-any.whl (16 kB)
#12 60.23 Collecting pexpect>4.3 (from ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/9e/c3/059298687310d527a58bb01f3b1965787ee3b40dce76752eda8b44e9a2c5/pexpect-4.9.0-py2.py3-none-any.whl (63 kB)
#12 60.23 Collecting wcwidth (from prompt-toolkit<3.1.0,>=3.0.41->ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/af/b5/123f13c975e9f27ab9c0770f514345bd406d0e8d3b7a0723af9d43f710af/wcwidth-0.2.14-py2.py3-none-any.whl (37 kB)
#12 60.23 Collecting parso<0.9.0,>=0.8.4 (from jedi>=0.16->ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/16/32/f8e3c85d1d5250232a5d3477a2a28cc291968ff175caeadaf3cc19ce0e4a/parso-0.8.5-py2.py3-none-any.whl (106 kB)
#12 60.23 Collecting ptyprocess>=0.5 (from pexpect>4.3->ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/22/a6/858897256d0deac81a172289110f31629fc4cee19b6f01283303e18c8db3/ptyprocess-0.7.0-py2.py3-none-any.whl (13 kB)
#12 60.23 Collecting MarkupSafe>=2.0 (from jinja2->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/6f/bc/4dc914ead3fe6ddaef035341fee0fc956949bbd27335b611829292b89ee2/markupsafe-3.0.3-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (20 kB)
#12 60.23 Collecting numpy>=1.22.4 (from pandas->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/b9/14/78635daab4b07c0930c919d451b8bf8c164774e6a3413aed04a6d95758ce/numpy-2.0.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (19.5 MB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 19.5/19.5 MB 7.9 MB/s  0:00:02
#12 60.23 Collecting tzdata>=2022.7 (from pandas->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c7/b0/003792df09decd6849a5e39c28b513c06e84436a54440380862b5aeff25d/tzdata-2025.3-py2.py3-none-any.whl (348 kB)
#12 60.23 Collecting charset_normalizer<4,>=2 (from requests->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/dd/21/0274deb1cc0632cd587a9a0ec6b4674d9108e461cb4cd40d457adaeb0564/charset_normalizer-3.4.4-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (153 kB)
#12 60.23 Collecting idna<4,>=2.5 (from requests->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/0e/61/66938bbb5fc52dbdf84594873d5b51fb1f7c7794e9c0f5bd885f30bc507b/idna-3.11-py3-none-any.whl (71 kB)
#12 60.23 Collecting urllib3<3,>=1.21.1 (from requests->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/6d/b9/4095b668ea3678bf6a0af005527f39de12fb026516fb3df17495a733b7f8/urllib3-2.6.2-py3-none-any.whl (131 kB)
#12 60.23 Collecting certifi>=2017.4.17 (from requests->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/70/7d/9bc192684cea499815ff478dfcdc13835ddf401365057044fb721ec6bddb/certifi-2025.11.12-py3-none-any.whl (159 kB)
#12 60.23 Collecting markdown-it-py>=2.2.0 (from rich[jupyter]->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/42/d7/1ec15b46af6af88f19b8e5ffea08fa375d433c998b8a7639e76935c14f1f/markdown_it_py-3.0.0-py3-none-any.whl (87 kB)
#12 60.23 Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich[jupyter]->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/b3/38/89ba8ad64ae25be8de66a6d463314cf1eb366222074cfda9ee839c56a4b4/mdurl-0.1.2-py3-none-any.whl (10.0 kB)
#12 60.23 Collecting ruamel.yaml.clib>=0.2.15 (from ruamel.yaml->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/ca/20/3e7b0d26261c2ac0c272f42f21408bf2d01aaa08cddd378a51056b3f5fbc/ruamel_yaml_clib-0.2.15-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (734 kB)
#12 60.23      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 734.1/734.1 kB 7.6 MB/s  0:00:00
#12 60.23 Collecting executing>=1.2.0 (from stack-data->ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/c1/ea/53f2148663b321f21b5a606bd5f191517cf40b7072c0497d3c92c4a13b1e/executing-2.2.1-py2.py3-none-any.whl (28 kB)
#12 60.23 Collecting asttokens>=2.1.0 (from stack-data->ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/d2/39/e7eaf1799466a4aef85b6a4fe7bd175ad2b1c6345066aa33f1f58d4b18d0/asttokens-3.0.1-py3-none-any.whl (27 kB)
#12 60.23 Collecting pure-eval (from stack-data->ipython>=6.1.0->ipywidgets->sqlmesh==0.147.1.dev1)
#12 60.23   Downloading http://mirrors.tools.huawei.com/pypi/packages/8e/37/efad0257dc6e593a18957422533ff0f87ede7c9c6ea010a2177d738fb82f/pure_eval-0.2.3-py3-none-any.whl (11 kB)
#12 60.23 Installing collected packages: pytz, pure-eval, ptyprocess, zipp, widgetsnbextension, wcwidth, urllib3, tzlocal, tzdata, typing-extensions, traitlets, tenacity, sqlglotrs, sqlglot, six, ruamel.yaml.clib, regex, pygments, pexpect, parso, numpy, mdurl, MarkupSafe, jupyterlab_widgets, idna, hyperscript, executing, duckdb, decorator, comm, click, charset_normalizer, certifi, asttokens, astor, annotated-types, typing-inspection, stack-data, ruamel.yaml, requests, python-dateutil, pydantic-core, prompt-toolkit, matplotlib-inline, markdown-it-py, jinja2, jedi, importlib-metadata, exceptiongroup, time-machine, rich, pydantic, pandas, ipython, dateparser, croniter, ipywidgets, sqlmesh
#12 60.23   Running setup.py develop for sqlmesh
#12 60.23 
#12 60.23 Successfully installed MarkupSafe-3.0.3 annotated-types-0.7.0 astor-0.8.1 asttokens-3.0.1 certifi-2025.11.12 charset_normalizer-3.4.4 click-8.1.8 comm-0.2.3 croniter-6.0.0 dateparser-1.2.2 decorator-5.2.1 duckdb-1.4.3 exceptiongroup-1.3.1 executing-2.2.1 hyperscript-0.3.0 idna-3.11 importlib-metadata-8.7.1 ipython-8.18.1 ipywidgets-8.1.8 jedi-0.19.2 jinja2-3.1.6 jupyterlab_widgets-3.0.16 markdown-it-py-3.0.0 matplotlib-inline-0.2.1 mdurl-0.1.2 numpy-2.0.2 pandas-2.3.3 parso-0.8.5 pexpect-4.9.0 prompt-toolkit-3.0.52 ptyprocess-0.7.0 pure-eval-0.2.3 pydantic-2.12.5 pydantic-core-2.41.5 pygments-2.19.2 python-dateutil-2.9.0.post0 pytz-2025.2 regex-2025.11.3 requests-2.32.5 rich-14.2.0 ruamel.yaml-0.18.17 ruamel.yaml.clib-0.2.15 six-1.17.0 sqlglot-26.2.1 sqlglotrs-0.3.5 sqlmesh-0.147.1.dev1 stack-data-0.6.3 tenacity-9.1.2 time-machine-2.19.0 traitlets-5.14.3 typing-extensions-4.15.0 typing-inspection-0.4.2 tzdata-2025.3 tzlocal-5.3.1 urllib3-2.6.2 wcwidth-0.2.14 widgetsnbextension-4.0.15 zipp-3.23.0
#12 60.23 
#12 63.84   DEPRECATION: Legacy editable install of custom_materializations==0.0.0 from file:///testbed/TobikoData/sqlmesh/examples/custom_materializations (setup.py develop) is deprecated. pip 25.3 will enforce this behaviour change. A possible replacement is to add a pyproject.toml or enable --use-pep517, and use setuptools >= 64. If the resulting installation is not behaving as expected, try using --config-settings editable_mode=compat. Please consult the setuptools documentation for more information. Discussion can be found at https://github.com/pypa/pip/issues/11457
#12 63.84 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#12 63.84 
#12 63.84 Looking in indexes: http://mirrors.tools.huawei.com/pypi/simple/
#12 63.84 Obtaining file:///testbed/TobikoData/sqlmesh/examples/custom_materializations
#12 63.84   Preparing metadata (setup.py): started
#12 63.84   Preparing metadata (setup.py): finished with status 'done'
#12 63.84 Requirement already satisfied: sqlmesh in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from custom_materializations==0.0.0) (0.147.1.dev1)
#12 63.84 Requirement already satisfied: astor in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (0.8.1)
#12 63.84 Requirement already satisfied: click in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (8.1.8)
#12 63.84 Requirement already satisfied: croniter in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (6.0.0)
#12 63.84 Requirement already satisfied: duckdb!=0.10.3 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (1.4.3)
#12 63.84 Requirement already satisfied: dateparser in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (1.2.2)
#12 63.84 Requirement already satisfied: hyperscript>=0.1.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (0.3.0)
#12 63.84 Requirement already satisfied: importlib-metadata in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (8.7.1)
#12 63.84 Requirement already satisfied: ipywidgets in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (8.1.8)
#12 63.84 Requirement already satisfied: jinja2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (3.1.6)
#12 63.84 Requirement already satisfied: pandas in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (2.3.3)
#12 63.84 Requirement already satisfied: pydantic>=2.0.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (2.12.5)
#12 63.84 Requirement already satisfied: requests in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (2.32.5)
#12 63.84 Requirement already satisfied: rich[jupyter] in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (14.2.0)
#12 63.84 Requirement already satisfied: ruamel.yaml in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (0.18.17)
#12 63.84 Requirement already satisfied: sqlglot~=26.2.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlglot[rs]~=26.2.1->sqlmesh->custom_materializations==0.0.0) (26.2.1)
#12 63.84 Requirement already satisfied: tenacity in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (9.1.2)
#12 63.84 Requirement already satisfied: time-machine in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlmesh->custom_materializations==0.0.0) (2.19.0)
#12 63.84 Requirement already satisfied: sqlglotrs==0.3.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from sqlglot[rs]~=26.2.1->sqlmesh->custom_materializations==0.0.0) (0.3.5)
#12 63.84 Requirement already satisfied: annotated-types>=0.6.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pydantic>=2.0.0->sqlmesh->custom_materializations==0.0.0) (0.7.0)
#12 63.84 Requirement already satisfied: pydantic-core==2.41.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pydantic>=2.0.0->sqlmesh->custom_materializations==0.0.0) (2.41.5)
#12 63.84 Requirement already satisfied: typing-extensions>=4.14.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pydantic>=2.0.0->sqlmesh->custom_materializations==0.0.0) (4.15.0)
#12 63.84 Requirement already satisfied: typing-inspection>=0.4.2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pydantic>=2.0.0->sqlmesh->custom_materializations==0.0.0) (0.4.2)
#12 63.84 Requirement already satisfied: python-dateutil in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from croniter->sqlmesh->custom_materializations==0.0.0) (2.9.0.post0)
#12 63.84 Requirement already satisfied: pytz>2021.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from croniter->sqlmesh->custom_materializations==0.0.0) (2025.2)
#12 63.84 Requirement already satisfied: regex>=2024.9.11 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from dateparser->sqlmesh->custom_materializations==0.0.0) (2025.11.3)
#12 63.84 Requirement already satisfied: tzlocal>=0.2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from dateparser->sqlmesh->custom_materializations==0.0.0) (5.3.1)
#12 63.84 Requirement already satisfied: six>=1.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from python-dateutil->croniter->sqlmesh->custom_materializations==0.0.0) (1.17.0)
#12 63.84 Requirement already satisfied: zipp>=3.20 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from importlib-metadata->sqlmesh->custom_materializations==0.0.0) (3.23.0)
#12 63.84 Requirement already satisfied: comm>=0.1.3 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.2.3)
#12 63.84 Requirement already satisfied: ipython>=6.1.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipywidgets->sqlmesh->custom_materializations==0.0.0) (8.18.1)
#12 63.84 Requirement already satisfied: traitlets>=4.3.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipywidgets->sqlmesh->custom_materializations==0.0.0) (5.14.3)
#12 63.84 Requirement already satisfied: widgetsnbextension~=4.0.14 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipywidgets->sqlmesh->custom_materializations==0.0.0) (4.0.15)
#12 63.84 Requirement already satisfied: jupyterlab_widgets~=3.0.15 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipywidgets->sqlmesh->custom_materializations==0.0.0) (3.0.16)
#12 63.84 Requirement already satisfied: decorator in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (5.2.1)
#12 63.84 Requirement already satisfied: jedi>=0.16 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.19.2)
#12 63.84 Requirement already satisfied: matplotlib-inline in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.2.1)
#12 63.84 Requirement already satisfied: prompt-toolkit<3.1.0,>=3.0.41 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (3.0.52)
#12 63.84 Requirement already satisfied: pygments>=2.4.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (2.19.2)
#12 63.84 Requirement already satisfied: stack-data in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.6.3)
#12 63.84 Requirement already satisfied: exceptiongroup in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (1.3.1)
#12 63.84 Requirement already satisfied: pexpect>4.3 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (4.9.0)
#12 63.84 Requirement already satisfied: wcwidth in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from prompt-toolkit<3.1.0,>=3.0.41->ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.2.14)
#12 63.84 Requirement already satisfied: parso<0.9.0,>=0.8.4 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from jedi>=0.16->ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.8.5)
#12 63.84 Requirement already satisfied: ptyprocess>=0.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pexpect>4.3->ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.7.0)
#12 63.84 Requirement already satisfied: MarkupSafe>=2.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from jinja2->sqlmesh->custom_materializations==0.0.0) (3.0.3)
#12 63.84 Requirement already satisfied: numpy>=1.22.4 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pandas->sqlmesh->custom_materializations==0.0.0) (2.0.2)
#12 63.84 Requirement already satisfied: tzdata>=2022.7 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pandas->sqlmesh->custom_materializations==0.0.0) (2025.3)
#12 63.84 Requirement already satisfied: charset_normalizer<4,>=2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests->sqlmesh->custom_materializations==0.0.0) (3.4.4)
#12 63.84 Requirement already satisfied: idna<4,>=2.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests->sqlmesh->custom_materializations==0.0.0) (3.11)
#12 63.84 Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests->sqlmesh->custom_materializations==0.0.0) (2.6.2)
#12 63.84 Requirement already satisfied: certifi>=2017.4.17 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests->sqlmesh->custom_materializations==0.0.0) (2025.11.12)
#12 63.84 Requirement already satisfied: markdown-it-py>=2.2.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from rich[jupyter]->sqlmesh->custom_materializations==0.0.0) (3.0.0)
#12 63.84 Requirement already satisfied: mdurl~=0.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from markdown-it-py>=2.2.0->rich[jupyter]->sqlmesh->custom_materializations==0.0.0) (0.1.2)
#12 63.84 Requirement already satisfied: ruamel.yaml.clib>=0.2.15 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from ruamel.yaml->sqlmesh->custom_materializations==0.0.0) (0.2.15)
#12 63.84 Requirement already satisfied: executing>=1.2.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from stack-data->ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (2.2.1)
#12 63.84 Requirement already satisfied: asttokens>=2.1.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from stack-data->ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (3.0.1)
#12 63.84 Requirement already satisfied: pure-eval in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from stack-data->ipython>=6.1.0->ipywidgets->sqlmesh->custom_materializations==0.0.0) (0.2.3)
#12 63.84 Installing collected packages: custom_materializations
#12 63.84   Running setup.py develop for custom_materializations
#12 63.84 Successfully installed custom_materializations-0.0.0
#12 63.84 
#12 77.64 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#12 77.64 
#12 77.64 Looking in indexes: http://mirrors.tools.huawei.com/pypi/simple/
#12 77.64 Collecting google-cloud-bigquery
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/73/d7/946707c45c0f673b4cf032463896475d709d637d84f456aef29992396607/google_cloud_bigquery-3.39.0-py3-none-any.whl (259 kB)
#12 77.64 Collecting google-api-core<3.0.0,>=2.11.1 (from google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/ed/d4/90197b416cb61cefd316964fd9e7bd8324bcbafabf40eef14a9f20b81974/google_api_core-2.28.1-py3-none-any.whl (173 kB)
#12 77.64 Collecting google-auth<3.0.0,>=2.14.1 (from google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/c6/97/451d55e05487a5cd6279a01a7e34921858b16f7dc8aa38a2c684743cd2b3/google_auth-2.45.0-py2.py3-none-any.whl (233 kB)
#12 77.64 Collecting google-cloud-core<3.0.0,>=2.4.1 (from google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/89/20/bfa472e327c8edee00f04beecc80baeddd2ab33ee0e86fd7654da49d45e9/google_cloud_core-2.5.0-py3-none-any.whl (29 kB)
#12 77.64 Collecting google-resumable-media<3.0.0,>=2.0.0 (from google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/1f/0b/93afde9cfe012260e9fe1522f35c9b72d6ee222f316586b1f23ecf44d518/google_resumable_media-2.8.0-py3-none-any.whl (81 kB)
#12 77.64 Collecting packaging>=24.2.0 (from google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/20/12/38679034af332785aac8774540895e234f4d07f7545804097de4b666afd8/packaging-25.0-py3-none-any.whl (66 kB)
#12 77.64 Requirement already satisfied: python-dateutil<3.0.0,>=2.8.2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from google-cloud-bigquery) (2.9.0.post0)
#12 77.64 Requirement already satisfied: requests<3.0.0,>=2.21.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from google-cloud-bigquery) (2.32.5)
#12 77.64 Collecting googleapis-common-protos<2.0.0,>=1.56.2 (from google-api-core<3.0.0,>=2.11.1->google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/c4/ab/09169d5a4612a5f92490806649ac8d41e3ec9129c636754575b3553f4ea4/googleapis_common_protos-1.72.0-py3-none-any.whl (297 kB)
#12 77.64 Collecting protobuf!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<7.0.0,>=3.19.5 (from google-api-core<3.0.0,>=2.11.1->google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/56/13/333b8f421738f149d4fe5e49553bc2a2ab75235486259f689b4b91f96cec/protobuf-6.33.2-cp39-abi3-manylinux2014_x86_64.whl (323 kB)
#12 77.64 Collecting proto-plus<2.0.0,>=1.22.3 (from google-api-core<3.0.0,>=2.11.1->google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/cd/24/3b7a0818484df9c28172857af32c2397b6d8fcd99d9468bd4684f98ebf0a/proto_plus-1.27.0-py3-none-any.whl (50 kB)
#12 77.64 Collecting grpcio<2.0.0,>=1.33.2 (from google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/e0/61/4cca38c4e7bb3ac5a1e0be6cf700a4dd85c61cbd8a9c5e076c224967084e/grpcio-1.76.0-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (6.6 MB)
#12 77.64      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 12.8 MB/s  0:00:00
#12 77.64 Collecting grpcio-status<2.0.0,>=1.33.2 (from google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/8c/cc/27ba60ad5a5f2067963e6a858743500df408eb5855e98be778eaef8c9b02/grpcio_status-1.76.0-py3-none-any.whl (14 kB)
#12 77.64 Collecting cachetools<7.0,>=2.0.0 (from google-auth<3.0.0,>=2.14.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/2c/fc/1d7b80d0eb7b714984ce40efc78859c022cd930e402f599d8ca9e39c78a4/cachetools-6.2.4-py3-none-any.whl (11 kB)
#12 77.64 Collecting pyasn1-modules>=0.2.1 (from google-auth<3.0.0,>=2.14.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/47/8d/d529b5d697919ba8c11ad626e835d4039be708a35b0d22de83a269a6682c/pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
#12 77.64 Collecting rsa<5,>=3.1.4 (from google-auth<3.0.0,>=2.14.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/64/8d/0133e4eb4beed9e425d9a98ed6e081a55d195481b7632472be1af08d2f6b/rsa-4.9.1-py3-none-any.whl (34 kB)
#12 77.64 Collecting google-crc32c<2.0.0,>=1.0.0 (from google-resumable-media<3.0.0,>=2.0.0->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/1e/c4/7032f0e87ee0b0f65669ac8a1022beabd80afe5da69f4bbf49eb7fea9c40/google_crc32c-1.8.0-cp39-cp39-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl (33 kB)
#12 77.64 Requirement already satisfied: typing-extensions~=4.12 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from grpcio<2.0.0,>=1.33.2->google-api-core[grpc]<3.0.0,>=2.11.1->google-cloud-bigquery) (4.15.0)
#12 77.64 Requirement already satisfied: six>=1.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from python-dateutil<3.0.0,>=2.8.2->google-cloud-bigquery) (1.17.0)
#12 77.64 Requirement already satisfied: charset_normalizer<4,>=2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests<3.0.0,>=2.21.0->google-cloud-bigquery) (3.4.4)
#12 77.64 Requirement already satisfied: idna<4,>=2.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests<3.0.0,>=2.21.0->google-cloud-bigquery) (3.11)
#12 77.64 Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests<3.0.0,>=2.21.0->google-cloud-bigquery) (2.6.2)
#12 77.64 Requirement already satisfied: certifi>=2017.4.17 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests<3.0.0,>=2.21.0->google-cloud-bigquery) (2025.11.12)
#12 77.64 Collecting pyasn1>=0.1.3 (from rsa<5,>=3.1.4->google-auth<3.0.0,>=2.14.1->google-cloud-bigquery)
#12 77.64   Downloading http://mirrors.tools.huawei.com/pypi/packages/c8/f1/d6a797abb14f6283c0ddff96bbdd46937f64122b8c925cab503dd37f8214/pyasn1-0.6.1-py3-none-any.whl (83 kB)
#12 77.64 Installing collected packages: pyasn1, protobuf, packaging, grpcio, google-crc32c, cachetools, rsa, pyasn1-modules, proto-plus, googleapis-common-protos, google-resumable-media, grpcio-status, google-auth, google-api-core, google-cloud-core, google-cloud-bigquery
#12 77.64 
#12 77.64 Successfully installed cachetools-6.2.4 google-api-core-2.28.1 google-auth-2.45.0 google-cloud-bigquery-3.39.0 google-cloud-core-2.5.0 google-crc32c-1.8.0 google-resumable-media-2.8.0 googleapis-common-protos-1.72.0 grpcio-1.76.0 grpcio-status-1.76.0 packaging-25.0 proto-plus-1.27.0 protobuf-6.33.2 pyasn1-0.6.1 pyasn1-modules-0.4.2 rsa-4.9.1
#12 77.64 
#12 82.86 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#12 82.86 
#12 82.86 Looking in indexes: http://mirrors.tools.huawei.com/pypi/simple/
#12 82.86 Collecting PyGithub
#12 82.86   Downloading http://mirrors.tools.huawei.com/pypi/packages/07/ba/7049ce39f653f6140aac4beb53a5aaf08b4407b6a3019aae394c1c5244ff/pygithub-2.8.1-py3-none-any.whl (432 kB)
#12 82.86 Collecting pynacl>=1.4.0 (from PyGithub)
#12 82.86   Downloading http://mirrors.tools.huawei.com/pypi/packages/a8/6c/dd9ee8214edf63ac563b08a9b30f98d116942b621d39a751ac3256694536/pynacl-1.6.1-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
#12 82.86      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 9.7 MB/s  0:00:00
#12 82.86 Requirement already satisfied: requests>=2.14.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from PyGithub) (2.32.5)
#12 82.86 Collecting pyjwt>=2.4.0 (from pyjwt[crypto]>=2.4.0->PyGithub)
#12 82.86   Downloading http://mirrors.tools.huawei.com/pypi/packages/61/ad/689f02752eeec26aed679477e80e632ef1b682313be70793d798c1d5fc8f/PyJWT-2.10.1-py3-none-any.whl (22 kB)
#12 82.86 Requirement already satisfied: typing-extensions>=4.5.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from PyGithub) (4.15.0)
#12 82.86 Requirement already satisfied: urllib3>=1.26.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from PyGithub) (2.6.2)
#12 82.86 Collecting cryptography>=3.4.0 (from pyjwt[crypto]>=2.4.0->PyGithub)
#12 82.86   Downloading http://mirrors.tools.huawei.com/pypi/packages/fc/59/873633f3f2dcd8a053b8dd1d38f783043b5fce589c0f6988bf55ef57e43e/cryptography-46.0.3-cp38-abi3-manylinux_2_34_x86_64.whl (4.5 MB)
#12 82.86      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 11.7 MB/s  0:00:00
#12 82.86 Collecting cffi>=2.0.0 (from cryptography>=3.4.0->pyjwt[crypto]>=2.4.0->PyGithub)
#12 82.86   Downloading http://mirrors.tools.huawei.com/pypi/packages/1f/74/cc4096ce66f5939042ae094e2e96f53426a979864aa1f96a621ad128be27/cffi-2.0.0-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (216 kB)
#12 82.86 Collecting pycparser (from cffi>=2.0.0->cryptography>=3.4.0->pyjwt[crypto]>=2.4.0->PyGithub)
#12 82.86   Downloading http://mirrors.tools.huawei.com/pypi/packages/a0/e3/59cd50310fc9b59512193629e1984c1f95e5c8ae6e5d8c69532ccc65a7fe/pycparser-2.23-py3-none-any.whl (118 kB)
#12 82.86 Requirement already satisfied: charset_normalizer<4,>=2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests>=2.14.0->PyGithub) (3.4.4)
#12 82.86 Requirement already satisfied: idna<4,>=2.5 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests>=2.14.0->PyGithub) (3.11)
#12 82.86 Requirement already satisfied: certifi>=2017.4.17 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from requests>=2.14.0->PyGithub) (2025.11.12)
#12 82.86 Installing collected packages: pyjwt, pycparser, cffi, pynacl, cryptography, PyGithub
#12 82.86 
#12 82.86 Successfully installed PyGithub-2.8.1 cffi-2.0.0 cryptography-46.0.3 pycparser-2.23 pyjwt-2.10.1 pynacl-1.6.1
#12 82.86 
#12 88.66 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#12 88.66 
#12 88.66 Looking in indexes: http://mirrors.tools.huawei.com/pypi/simple/
#12 88.66 Collecting pytest
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/a8/a4/20da314d277121d6534b3a980b29035dcd51e6744bd79075a6ce8fa4eb8d/pytest-8.4.2-py3-none-any.whl (365 kB)
#12 88.66 Collecting pytest-json-report
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/81/35/d07400c715bf8a88aa0c1ee9c9eb6050ca7fe5b39981f0eea773feeb0681/pytest_json_report-1.5.0-py3-none-any.whl (13 kB)
#12 88.66 Collecting toml
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/44/6f/7120676b6d73228c96e17f1f794d8ab046fc910d781c8d151120c3f1569e/toml-0.10.2-py2.py3-none-any.whl (16 kB)
#12 88.66 Collecting debugpy
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/3c/ab/7f3dccc256a18b535c915a84501925e50f95f0e4bc8b85779932a952b71f/debugpy-1.8.19-cp39-cp39-manylinux_2_34_x86_64.whl (3.1 MB)
#12 88.66      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.1/3.1 MB 15.1 MB/s  0:00:00
#12 88.66 Collecting pytest_mock
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/5a/cc/06253936f4a7fa2e0f48dfe6d851d9c56df896a9ab09ac019d70b760619c/pytest_mock-3.15.1-py3-none-any.whl (10 kB)
#12 88.66 Collecting pytest-xdist
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/ca/31/d4e37e9e550c2b92a9cbc2e4d0b7420a27224968580b5a447f420847c975/pytest_xdist-3.8.0-py3-none-any.whl (46 kB)
#12 88.66 Requirement already satisfied: exceptiongroup>=1 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pytest) (1.3.1)
#12 88.66 Collecting iniconfig>=1 (from pytest)
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/2c/e1/e6716421ea10d38022b952c159d5161ca1193197fb744506875fbb87ea7b/iniconfig-2.1.0-py3-none-any.whl (6.0 kB)
#12 88.66 Requirement already satisfied: packaging>=20 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pytest) (25.0)
#12 88.66 Collecting pluggy<2,>=1.5 (from pytest)
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/54/20/4d324d65cc6d9205fabedc306948156824eb9f0ee1633355a8f7ec5c66bf/pluggy-1.6.0-py3-none-any.whl (20 kB)
#12 88.66 Requirement already satisfied: pygments>=2.7.2 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from pytest) (2.19.2)
#12 88.66 Collecting tomli>=1 (from pytest)
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/77/b8/0135fadc89e73be292b473cb820b4f5a08197779206b33191e801feeae40/tomli-2.3.0-py3-none-any.whl (14 kB)
#12 88.66 Collecting pytest-metadata (from pytest-json-report)
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/3e/43/7e7b2ec865caa92f67b8f0e9231a798d102724ca4c0e1f414316be1c1ef2/pytest_metadata-3.1.1-py3-none-any.whl (11 kB)
#12 88.66 Collecting execnet>=2.1 (from pytest-xdist)
#12 88.66   Downloading http://mirrors.tools.huawei.com/pypi/packages/ab/84/02fc1827e8cdded4aa65baef11296a9bbe595c474f0d6d758af082d849fd/execnet-2.1.2-py3-none-any.whl (40 kB)
#12 88.66 Requirement already satisfied: typing-extensions>=4.6.0 in /opt/miniconda3/envs/testbed/lib/python3.9/site-packages (from exceptiongroup>=1->pytest) (4.15.0)
#12 88.66 Installing collected packages: tomli, toml, pluggy, iniconfig, execnet, debugpy, pytest, pytest-xdist, pytest_mock, pytest-metadata, pytest-json-report
#12 88.66 
#12 88.66 Successfully installed debugpy-1.8.19 execnet-2.1.2 iniconfig-2.1.0 pluggy-1.6.0 pytest-8.4.2 pytest-json-report-1.5.0 pytest-metadata-3.1.1 pytest-xdist-3.8.0 pytest_mock-3.15.1 toml-0.10.2 tomli-2.3.0
#12 88.66 
#12 DONE 88.9s

#13 [ 9/10] WORKDIR /testbed
#13 DONE 0.1s

#14 [10/10] RUN echo "conda activate testbed" >> /root/.bashrc
#14 DONE 0.3s

#15 exporting to image
#15 exporting layers
#15 exporting layers 15.0s done
#15 exporting manifest sha256:3b7619bdde3a8ae94cbde3a66ef97df562428cf8439de62a11140bfc60284631 0.0s done
#15 exporting config sha256:32538633f35d080c42d842662e5dd8450e242ad5158f9656711bad844aa8920b 0.0s done
#15 exporting attestation manifest sha256:2feb7b781ca6a1848d81c27863041acc49f9a9795fa9ccf2d424c0127240e924 0.0s done
#15 exporting manifest list sha256:43687424fba1f19b645e5d20ed5d6c686b6b40c887986cba666d9daebe660123 0.0s done
#15 naming to docker.io/library/sqlmesh:3.9_default
#15 naming to docker.io/library/sqlmesh:3.9_default done
#15 unpacking to docker.io/library/sqlmesh:3.9_default
#15 unpacking to docker.io/library/sqlmesh:3.9_default 5.6s done
#15 DONE 20.8s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/u7frfbgpbp7p2cn65b95ilfiy
