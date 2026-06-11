from typing import Optional

from tinygrad.dtype import dtypes, DType, truncate
from tinygrad.uop import auto, FastEnum, GroupOp, Ops
from tinygrad.uop.ops import UOp, UPat, PatternMatcher
from tinygrad.renderer.isa import Register, IselContext

# ***** RDNA3 Ops *****

class RDNA3Ops(FastEnum):
    # ** SOP2 - 2in - 1out - 32bit literals **
    S_ADD_U32 = auto(); S_SUB_U32 = auto(); S_ADD_I32 = auto()
    S_SUB_I32 = auto(); S_AND_B32 = auto(); S_OR_B32 = auto(); S_XOR_B32 = auto()
    S_LSHL_B32 = auto(); S_LSHR_B32 = auto(); S_ASHR_I32 = auto()

    # ** SOP1 - 1in - 1out - 32bit literals **
    S_MOV_B32 = auto(); S_MOV_B64 = auto(); S_CMOV_B32 = auto(); S_NOT_B32 = auto()
    S_AND_SAVEEXEC_B64 = auto(); S_OR_SAVEEXEC_B64 = auto(); S_XOR_SAVEEXEC_B64 = auto()

    # ** SOPC - 2in - 1out SCC - 32bit literals **
    S_CMP_EQ_I32 = auto(); S_CMP_LG_I32 = auto(); S_CMP_GT_I32 = auto()
    S_CMP_GE_I32 = auto(); S_CMP_LT_I32 = auto(); S_CMP_LE_I32 = auto()
    S_CMP_EQ_U32 = auto(); S_CMP_LG_U32 = auto(); S_CMP_GT_U32 = auto()
    S_CMP_GE_U32 = auto(); S_CMP_LT_U32 = auto(); S_CMP_LE_U32 = auto()

    # ** SOPP - 1in - control flow - SIMM16 **
    S_NOP = auto(); S_ENDPGM = auto(); S_WAITCNT = auto(); S_BARRIER = auto()
    S_BRANCH = auto(); S_CBRANCH_SCC0 = auto(); S_CBRANCH_SCC1 = auto()
    S_CBRANCH_EXECZ = auto(); S_CBRANCH_EXECNZ = auto()

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

# ***** RDNA3 groups *****
VALU_RESULT_OPS = {
  RDNA3Ops.V_MOV_B32,
  RDNA3Ops.V_MOV_B16,
  RDNA3Ops.V_ADD_F32,
  RDNA3Ops.V_SUB_F32,
  RDNA3Ops.V_MUL_F32,
  RDNA3Ops.V_ADD_NC_U32,
  RDNA3Ops.V_SUB_NC_U32,
  RDNA3Ops.GLOBAL_LOAD_B32,
}

SALU_RESULT_OPS = {
  RDNA3Ops.S_MOV_B32,
  RDNA3Ops.S_MOV_B64,
  RDNA3Ops.S_ADD_U32,
  RDNA3Ops.S_SUB_U32,
  RDNA3Ops.S_LOAD_B32,
}

VCC_RESULT_OPS = {
  RDNA3Ops.V_CMP_LT_F32,
  RDNA3Ops.V_CMP_EQ_F32,
  RDNA3Ops.V_CMP_NEQ_F32,
  RDNA3Ops.V_CMP_LT_I32,
  RDNA3Ops.V_CMP_EQ_I32,
}

NO_RESULT_OPS = {
  RDNA3Ops.GLOBAL_STORE_B32,
  RDNA3Ops.S_WAITCNT,
  RDNA3Ops.S_BRANCH,
  RDNA3Ops.S_ENDPGM,
}
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

# ***** RDNA3 legalization *****

extra_matcher = PatternMatcher([
  # bool CMPNE is XOR, bool CMPEQ is XOR+XOR, bool CMPLT is XOR+AND
  # bool comparison lowering
  (UPat.var('x', dtypes.bool).ne(UPat.var('y')), lambda x,y: x^y),
  (UPat.var('x', dtypes.bool).alu(Ops.CMPEQ, UPat.var('y')), lambda x,y: (x^y)^True),
  (UPat.var('x', dtypes.bool)<UPat.var('y'), lambda x,y: (x^True)&y),
  # unsupported conversions
  # float16 -> int32/unsigned int32
  (UPat.var("y", dtypes.float16).cast(dtypes.int32s + dtypes.uint32s, name="x"),
   lambda y,x: y.cast(dtypes.float32).cast(x.dtype)),
  # int32/unsigned int32 -> float16
  (UPat.var("x", dtypes.int32s + dtypes.uint32s).cast(dtypes.float16, name="y"),
   lambda x,y: x.cast(dtypes.float32).cast(y.dtype)),
  # from x86
  # rewrite -x -> 0 - x
  (UPat(Ops.NEG, name="x"), lambda x: UOp(Ops.SUB, x.dtype, (x.const_like(0),) + x.src)),
  # rewrite modulo as dividend - divisor * quotient
  (UPat(Ops.CMOD, src=(UPat.var("x"), UPat.var("y"))), lambda x,y: x - y * x.alu(Ops.CDIV, y)),

])

# ***** RDNA3 pre instruction selection *****

pre_isel_matcher = PatternMatcher([
  # noop of a noop is removed
  (UPat(Ops.NOOP, src=(UPat(Ops.NOOP),), name="x"), lambda x: x.replace(src=x.src[0].src)),
  # cast between signed and unsigned int is a noop
  (UPat.var("y", dtypes.ints+(dtypes.bool,)).cast(dtypes.ints, name="x"),
   lambda y,x: x.replace(op=Ops.NOOP) if x.dtype.itemsize == y.dtype.itemsize else None),
  # same-size bitcasts are usually noops on VGPRs
  (UPat.var("y").bitcast().named("x"),
   lambda y,x: x.replace(op=Ops.NOOP) if x.dtype.itemsize == y.dtype.itemsize else None),
  # raw bool where needs a compare so it can become VCC
  (UPat.var("m", dtypes.bool).where(UPat.var("a"), UPat.var("b")),
   lambda m,a,b: m.ne(0).where(a,b) if m.op not in GroupOp.Comparison and a.dtype.count == 1 else None),
])

# ***** RDNA3 instruction selection *****

# registry ops
def def_reg(dt: DType, reg: Optional[Register]=None):
    return UOp(Ops.DEFINE_VAR, dt, tag=None if reg is None else (reg,))

# immediate constant
def imm(dt: DType, value: int):
    return UOp.const(dt, truncate[dt](value)).rtag()
def to_imm(c:UOp) -> UOp|None:
  if c.op is not Ops.CONST: return None
  if c.dtype in dtypes.ints+(dtypes.bool,): return imm(c.dtype, c.arg)
  return None

# type mapping
def rdna3_cmp_op(x:UOp) -> RDNA3Ops:
  dt = x.src[0].dtype
  if x.op is Ops.CMPEQ:
    if dt is dtypes.float32: return RDNA3Ops.V_CMP_EQ_F32
    if dt is dtypes.int32: return RDNA3Ops.V_CMP_EQ_I32
    if dt is dtypes.uint32: return RDNA3Ops.V_CMP_EQ_U32
  if x.op is Ops.CMPNE:
    if dt is dtypes.float32: return RDNA3Ops.V_CMP_NEQ_F32
    if dt is dtypes.int32: return RDNA3Ops.V_CMP_NE_I32
    if dt is dtypes.uint32: return RDNA3Ops.V_CMP_NE_U32
  if x.op is Ops.CMPLT:
    if dt is dtypes.float32: return RDNA3Ops.V_CMP_LT_F32
    if dt is dtypes.int32: return RDNA3Ops.V_CMP_LT_I32
    if dt is dtypes.uint32: return RDNA3Ops.V_CMP_LT_U32
  raise NotImplementedError(f"unsupported RDNA3 cmp {x.op} {dt}")

# get addr
# spgr pointer and vgpr byte offset
def rdna3_addr(x:UOp) -> tuple[UOp, ...]:
  def _offset(v:int): return imm(dtypes.int32, v)
  if x.op is not Ops.INDEX: return (x, UOp(Ops.NOOP), _offset(0))
  base, idx = x.src
  itemsize = base.dtype.itemsize if isinstance(base.dtype, dtypes.Array) else 1
  addr_offset = 0
  if idx.op is Ops.ADD and idx.src[0].op is Ops.INDEX:
    var_idx = idx.src[0]
    const_idx = idx.src[1].arg
    byte_offset = (var_idx if itemsize == 1 else var_idx * var_idx.const_like(itemsize))
    const_bytes = const_idx * itemsize
    if -4096 <= const_idx <= 4095:
      addr_offset = const_bytes
    else:
      byte_offset = byte_offset + byte_offset.const_like(const_bytes)
  else:
    byte_offset = idx if itemsize == 1 else idx * idx.const_like(itemsize)

  return (byte_offset, base, _offset(addr_offset))
   
def alloc_vregs(ctx:IselContext, x:UOp) -> UOp|None:
  if x.op is Ops.DEFINE_REG and x.tag is not None:
    return None
  if x.dtype is dtypes.void: return None
  if isinstance(x.tag, tuple) and x.tag[0]._cons: return None
  if x.arg in NO_RESULT_OPS: return None

  if x.arg in VALU_RESULT_OPS:
    return x.replace(tag=ctx.vreg(ALLOC_VGPR))
  if x.arg in SALU_RESULT_OPS:
    return x.replace(tag=ctx.sreg(ALLOC_SGPR))
  if x.arg in VCC_RESULT_OPS:
    return x.replace(tag=(ctx.vreg(VCC),))
  
  raise NotImplementedError(
    f"no RDNA3 destination register class for {x.arg}"
  )