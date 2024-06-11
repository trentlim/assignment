import pytest
import os
import pathlib
import shutil


@pytest.fixture(scope="session", autouse=True)
def tmp_test_data_dir(request, tmp_path_factory):  # pragma: no cover
    """
    This is a fixture which uses the pytest tmp_path_factory fixture
    and extends it by copying the entire contents of the test_data
    directory. After the test session is finished, then it calls
    the `cleaup_tmp` method which tears down the fixture and cleans up itself.
    """

    use_temp_dir = True
    if use_temp_dir:
        temp_data_dir = tmp_path_factory.mktemp("temp_data")

        def cleanup_tmp():
            if os.path.exists(temp_data_dir):
                shutil.rmtree(temp_data_dir)

        request.addfinalizer(cleanup_tmp)
    else:
        datadir = os.path.join(pathlib.Path.home(), "quantify_schedule_test")
        if not os.path.isdir(datadir):
            os.mkdir(datadir)

        print(f"Data directory set to: {datadir}")
        temp_data_dir = datadir

    return temp_data_dir
