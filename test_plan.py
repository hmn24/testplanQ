#!/usr/bin/env python
"""
Demostrates KDB cross-processes driver usage from within the testcases.
"""

import sys

from testplan.testing.multitest import MultiTest

from testplan import test_plan
from testplan.testing.multitest import testsuite, testcase
from testplan.report.testing.styles import Style, StyleEnum

# Python script to start kdb processes
import startKdbProcesses as kdb

# Can investigate testcases by slotting in this line: import code; code.interact(local=locals())

OUTPUT_STYLE = Style(StyleEnum.ASSERTION_DETAIL, StyleEnum.ASSERTION_DETAIL)

INITIAL_CONTEXT = {
    'kdbTp': dict(proc='TP', cmd=['kdb-tick/tick.q'], port=5010),
    'kdbRdb': dict(proc='RDB', cmd=['kdb-tick/tick/r.q'], port=5011),
 }

@testsuite
class KdbQueries(object):
    """Suite that contains testcases that perform kdb queries."""

    def setup(self, env, result):
        """
        Setup method that will be executed before all testcases. It is
        used to create the processes that the testcases require.
        Parameters to be passed into kdbProc function comes from INITIAL_CONTEXT defined above
        """
        self.kdbTpObj = kdb.kdbProc(**env.kdbTp)
        self.kdbTpObj.startProc()
        self.kdbRdbObj = kdb.kdbProc(**env.kdbRdb)
        self.kdbRdbObj.startProc()

    @testcase
    def TP_loaded_successfully(self, env, result):
        """Ensure TP loads successfully"""
        # Check schema
        result.true(self.kdbTpObj.syncQueryProc('all `time`sym`price`size in cols trade'), description="Schema of TP trade table is correct")
        result.true(self.kdbTpObj.syncQueryProc('all `time`sym`src`bid`ask`bsize`asize in cols quote'), description="Schema of TP quote table is correct")

        # Check connected to RDB
        result.true(self.kdbTpObj.syncQueryProc('all 0 < count each .u.w'), description="Check subscription to TP by RDB")

    @testcase
    def RDB_loaded_successfully(self, env, result):
        """Ensure RDB loads successfully"""
        # Check schema
        result.true(self.kdbRdbObj.syncQueryProc('all `time`sym`price`size in cols trade'), description="Schema of RDB trade table is correct")
        result.true(self.kdbRdbObj.syncQueryProc('all `time`sym`src`bid`ask`bsize`asize in cols quote'), description="Schema of RDB quote table is correct")

    def teardown(self, env):
        self.kdbTpObj.stopProc()
        self.kdbRdbObj.stopProc()
        
# Hard-coding `pdf_path`, 'stdout_style' and 'pdf_style' so that the
# downloadable example gives meaningful and presentable output.
# NOTE: this programmatic arguments passing approach will cause Testplan
# to ignore any command line arguments related to that functionality.
@test_plan(
    name="KdbQueriesExample",
    stdout_style=OUTPUT_STYLE,
    pdf_style=OUTPUT_STYLE,
    pdf_path="report.pdf",
)
def main(plan):
    """
    Testplan decorated main function to add and execute MultiTests.

    :return: Testplan result object.
    :rtype:  ``testplan.base.TestplanResult``
    """
    plan.add(
        MultiTest(
            name="KdbQueriesTest",
            suites=[KdbQueries()],
            initial_context=INITIAL_CONTEXT,
        )
    )

if __name__ == "__main__":
    sys.exit(not main())
