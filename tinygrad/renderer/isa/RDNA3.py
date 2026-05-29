from tinygrad.dtype import dtypes
from tinygrad.uop import auto, FastEnum, GroupOp, Ops
from tinygrad.uop.ops import UOp, UPat, PatternMatcher
from tinygrad.renderer.isa import Register

# ***** RDNA3 Ops *****
# small endian
class RDNA3Ops(FastEnum):
    # ** SOP2 - 2in - 1out - 32bit literals **
    S_ADD_U32 = auto(); S_SUB_U32 = auto(); S_ADD_I32 = auto()
    S_SUB_I32 = auto(); S_AND_B32 = auto(); S_OR_B32 = auto(); S_XOR_B32 = auto()
    S_LSHL_B32 = auto(); S_LSHR_B32 = auto(); S_ASHR_I32 = auto()

    # ** SOP1 - 1in - 1out - 32bit literals **
    S_MOV_B32 = auto(); S_MOV_B64 = auto(); S_CMOV_B32 = auto(); S_NOT_B32 = auto();

    # ** SOPC - 2in - 1out SCC - 32bit literals **
    S_CMP_EQ_I32 = auto(); S_CMP_LG_I32 = auto(); S_CMP_GT_I32 = auto()
    S_CMP_GE_I32 = auto(); S_CMP_LT_I32 = auto(); S_CMP_LE_I32 = auto()
    S_CMP_EQ_U32 = auto(); S_CMP_LG_U32 = auto(); S_CMP_GT_U32 = auto()
    S_CMP_GE_U32 = auto(); S_CMP_LT_U32 = auto(); S_CMP_LE_U32 = auto()

    # ** SOPP - 1in - control flow - SIMM16 **
    S_NOP = auto(); S_ENDPGM = auto(); S_WAITCNT = auto(); S_BARRIER = auto()
    S_BRANCH = auto(); S_CBRANCH_SCC0 = auto(); S_CBRANCH_SCC1 = auto()

    # ** SMEM - memory in - SGPR out **
    S_LOAD_B32 = auto(); S_LOAD_B64 = auto(); S_LOAD_B128 = auto()

    # ** VOP2 - 2in - 1out - 32bit literals, DPP **
    V_ADD_F32 = auto(); V_SUB_F32 = auto(); V_MUL_F32 = auto(); V_FMAC_F32 = auto()
    V_MIN_F32 = auto(); V_MAX_F32 = auto(); V_SQRT_F32 = auto()
    V_ADD_F16 = auto(); V_SUB_F16 = auto(); V_MUL_F16 = auto(); V_FMAC_F16 = auto()
    V_MIN_F16 = auto(); V_MAX_F16 = auto(); V_SQRT_F16 = auto()
    V_ADD_NC_U32 = auto(); V_SUB_NC_U32 = auto(); V_MUL_LO_U32 = auto()
    V_AND_B32 = auto(); V_OR_B32 = auto(); V_XOR_B32 = auto()
    V_CNDMASK_B32 = auto()

    # ** VOP1 - 1in - 1out - 32bit literals, DPP **
    V_MOV_B32 = auto(); V_MOV_B16 = auto(); V_NOP = auto(); V_NOT_B32 = auto();
    V_CVT_F32_I32 = auto(); V_CVT_F32_U32 = auto(); V_CVT_I32_F32 = auto()
    V_CVT_U32_F32 = auto(); V_CVT_F16_F32 = auto(); V_CVT_F32_F16 = auto()

    # ** VOPC - 2in - 1out VCC - 32bit literals **
    V_CMP_LT_F32 = auto(); V_CMP_EQ_F32 = auto(); V_CMP_LE_F32 = auto()
    V_CMP_GT_F32 = auto(); V_CMP_GE_F32 = auto(); V_CMP_NEQ_F32 = auto()
    V_CMP_LT_I32 = auto(); V_CMP_EQ_I32 = auto(); V_CMP_LE_I32 = auto()
    V_CMP_GT_I32 = auto(); V_CMP_NE_I32 = auto(); V_CMP_GE_I32 = auto()
    V_CMP_LT_U32 = auto(); V_CMP_EQ_U32 = auto(); V_CMP_LE_U32 = auto()
    V_CMP_GT_U32 = auto(); V_CMP_NE_U32 = auto(); V_CMP_GE_U32 = auto()

    # ** VOP3 - 2/3in - 1out - 64bit encoding **
    V_ADD_NC_U16 = auto(); V_SUB_NC_U16 = auto(); V_MUL_LO_U16 = auto()

    # ** GLOBAL - global memory in - VGPR out **
    GLOBAL_LOAD_U8 = auto(); GLOBAL_LOAD_I8 = auto(); GLOBAL_LOAD_U16 = auto()
    GLOBAL_LOAD_I16 = auto(); GLOBAL_LOAD_B32 = auto(); GLOBAL_LOAD_B64 = auto()
    GLOBAL_LOAD_B96 = auto(); GLOBAL_LOAD_B128 = auto(); GLOBAL_STORE_B8 = auto()
    GLOBAL_STORE_B16 = auto(); GLOBAL_STORE_B32 = auto(); GLOBAL_STORE_B64 = auto()
    GLOBAL_STORE_B96 = auto(); GLOBAL_STORE_B128 = auto()

# ***** RDNA3 registers *****

SGPR = tuple(Register(f"s{i}", i) for i in range(106))
VGPR = tuple(Register(f"v{i}", 256 + i) for i in range(256))

VCC_LO = Register("vcc_lo", 106)
VCC_HI = Register("vcc_hi", 107)
VCC = Register("vcc", 106, (VCC_LO, VCC_HI))

EXEC_LO = Register("exec_lo", 126)
EXEC_HI = Register("exec_hi", 127)
EXEC = Register("exec", 126, (EXEC_LO, EXEC_HI))

SCC = Register("scc", 253)
M0 = Register("m0", 125)
NULL = Register("null", 124)
OFF = NULL
LIT = Register("lit", 255)

ALLOC_SGPR = SGPR[:96]
ALLOC_VGPR = VGPR

SPECIAL_SGPR = (
  VCC_LO, VCC_HI, VCC,
  EXEC_LO, EXEC_HI, EXEC,
  SCC, M0, NULL, OFF, LIT,
)
