from miasm.analysis.binary import Container
from miasm.analysis.machine import Machine
from miasm.core.locationdb import LocationDB
from miasm.ir.symbexec import SymbolicExecutionEngine
from miasm.ir.translators.z3_ir import TranslatorZ3
from msynth import Simplifier
from z3 import simplify


def getRaxExpr(file_path, start_addr):
    loc_db = LocationDB()
    container = Container.from_stream(open(file_path, 'rb'), loc_db)
    machine = Machine(container.arch)
    mdis = machine.dis_engine(container.bin_stream, loc_db=loc_db)
    lifter = machine.ira(mdis.loc_db)
    asm_block = mdis.dis_block(start_addr)

    ira_cfg = lifter.new_ircfg()
    lifter.add_asmblock_to_ircfg(asm_block, ira_cfg)

    sb = SymbolicExecutionEngine(lifter)
    sb.run_block_at(ira_cfg, start_addr)
    return sb.eval_exprid(lifter.arch.regs.RAX)


file_path = "./mba_challenge"
addr = 0x00001290

get_rax_output = getRaxExpr(file_path, addr)
simplifier = Simplifier("<your oracle.pickle path>")
print(simplifier.simplify(get_rax_output))