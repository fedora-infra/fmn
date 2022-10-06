from unittest import mock

import pytest

from fmn.api.database import gen_db_session


@pytest.mark.parametrize("testcase", ("happy-path", "exception-thrown", "commit-raises-exception"))
@mock.patch("fmn.api.database.async_session_maker")
async def test_gen_db_session(async_session_maker, testcase):
    mock_session = mock.AsyncMock()
    async_session_maker.return_value = mock_session

    if testcase == "happy-path":
        expectation = pytest.raises(StopAsyncIteration)
    else:
        expectation = pytest.raises(Exception)

    if "commit-raises-exception" in testcase:
        mock_session.commit.side_effect = Exception("BOO")

    agen = gen_db_session()

    db_session = await agen.asend(None)

    assert db_session is mock_session

    with expectation:
        if "thrown" not in testcase:
            await agen.asend(None)
        else:
            await agen.athrow(Exception("FOO"))

    if "exception" in testcase:
        mock_session.rollback.assert_awaited_with()
    else:
        mock_session.rollback.assert_not_awaited()

    mock_session.close.assert_awaited_with()
