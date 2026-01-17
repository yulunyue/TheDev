# zb run_one
``` xx
python -m tool.zb_main error key=.*failed:.*
```
# zb run_one fail
``` xx
python -m tool.zb_main run_all key=.*4847.*
```
# zb query_log fail
``` xx
python -m tool.zb_main query_log
```
# zb show_pre
``` xx
python -m tool.zb_main show_pre key=.*5115_4363_failed.*
```
# zb run_all REJECT
``` deep-ml
python -m tool.zb_main run_all key=.*DOCKER_BUILD_FAILED.*
```
# ciff value
```
python -m tool.zb_main view
```
# ciff policy
```
python -m tool.zb_main view
```

# ga done
```ga
python -m tool.pytest_main .*git_api.*
```

# thread poll
```ga
python -m tool.pytest_main .*thread_poll.*
```

