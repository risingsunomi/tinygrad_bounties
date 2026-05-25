from tinygrad.uop import auto, FastEnum

# ***** RDNA3 Ops *****
# small endian
class RDNA3Ops(FastEnum):
    # ** SOP2 - 2in - 1out - 32bit literals **
    S_ADD_U32 = auto(); S_SUB_U32 = auto(); S_ADD_I32 = auto()
    S_SUB_I32 = auto(); S_ADDC_U32 = auto(); S_SUBB_U32 = auto()
    S_ABSDIFF_I32 = auto(); S_LSHL_B32 = auto(); S_LSHL_B64 = auto()
    S_LSHR_B32 = auto(); S_LSHR_B64 = auto(); S_ASHR_I32 = auto()
    S_ASHR_I64 = auto(); S_LSHL1_ADD_U32 = auto(); S_LSHL2_ADD_U32 = auto()
    S_LSHL3_ADD_U32 = auto(); S_LSHL4_ADD_U32 = auto(); S_MIN_I32 = auto()
    S_MIN_U32 = auto(); S_MAX_I32 = auto(); S_MAX_U32 = auto()
    S_AND_B32 = auto(); S_AND_B64 = auto(); S_OR_B32 = auto(); S_OR_B64 = auto()
    S_XOR_B32 = auto(); S_XOR_B64 = auto(); S_XOR_B64 = auto()
    S_NAND_B32 = auto(); S_NAND_B64 = auto(); S_NOR_B32 = auto()
    S_NOR_B64 = auto(); S_XNOR_B32 = auto(); S_XNOR_B64 = auto()
    S_AND_NOTI_B32 = auto(); S_AND_NOTI_B64 = auto(); S_OR_NOTI_B32 = auto()
    S_OR_NOTI_B64 = auto(); S_BFE_U32 = auto(); S_BFE_I32 = auto()
    S_BFE_I64 = auto(); S_BFM_B32 = auto(); S_BFM_B64 = auto()
    S_MUL_I32 = auto(); S_MUL_HI_U32 = auto(); S_MUL_HI_I32 = auto()
    S_CSELECT_B32 = auto(); S_CSELECT_B64 = auto(); S_PACK_LL_B32_B16 = auto()
    S_PACK_LH_B32_B16 = auto(); S_PACK_HH_B32_B16 = auto(); S_PACK_HL_B32_B16 = auto() 

    # ** SOPK - 1in - 1 out - SIMM16 **
    S_MOVK_I32 = auto(); S_VERSION = auto(); S_CMOVE_I32 = auto()
    S_CMPK_EQ_I32 = auto(); S_CMPK_LG_I32 = auto(); S_CMPK_GT_I32 = auto()
    S_CMPK_GE_I32 = auto(); S_CMPK_LT_I32 = auto(); S_CMPK_LE_I32 = auto()
    S_CMPK_EQ_U32 = auto(); S_CMPK_LG_U32 = auto(); S_CMPK_GT_U32 = auto()
    S_CMPK_GE_U32 = auto(); S_CMPK_LT_U32 = auto(); S_CMPK_LE_U32 = auto()
    S_ADDK_I32 = auto(); S_MULK_I32 = auto(); S_GETREG_B32 = auto()
    S_SETREG_B32 = auto(); S_SETREG_IMM32_B32 = auto(); S_CALL_B64 = auto()
    S_WAITCNT_VSCNT = auto(); S_WAITCNT_VMCNT = auto(); S_WAITCNT_EXPCNT = auto()
    S_WAITCNT_LGKMCNT = auto()

    # ** SOP1 - 2in - 1out - 32bit literals **
    S_MOV_B32 = auto(); S_MOV_B64 = auto(); S_CMOV_B32 = auto()
    S_CMOV_B64 = auto(); S_BREV_B32 = auto(); S_BREV_B64 = auto()
    S_CTZ_I32_B32 = auto(); S_CTZ_I32_B64 = auto(); S_CTZ_I32_U32 = auto()
    S_CTZ_I32_U64 = auto(); S_CLS_I32 = auto(); S_CLS_I32_I64 = auto()
    S_SEXT_I32_I8 = auto(); S_SEXT_I32_I16 = auto(); S_BITSET0_B32 = auto()
    S_BITSET0_B64 = auto(); S_BITSET1_B32 = auto(); S_BITSET1_B64 = auto()
    S_BITREPLICATE_B64_B32 = auto(); S_ABS_I32 = auto(); S_BCNT0_I32_B32 = auto()
    S_BCNT0_I32_B64 = auto(); S_BCNT1_I32_B32 = auto(); S_BCNT1_I32_B64 = auto()
    S_QUADMASK_B32 = auto(); S_QUADMASK_B64 = auto(); S_WQM_B32 = auto()
    S_WQM_B64 = auto(); S_NOT_B32 = auto(); S_NOT_B64 = auto()
    S_AND_SAVEEXEC_B32 = auto(); S_AND_SAVEEXEC_B64 = auto(); S_OR_SAVEEXEC_B32 = auto()
    S_OR_SAVEEXEC_B64 = auto(); S_XOR_SAVEEXEC_B32 = auto(); S_XOR_SAVEEXEC_B64 = auto()
    S_NAND_SAVEEXEC_B32 = auto(); S_NAND_SAVEEXEC_B64 = auto()
    S_NOR_SAVEEXEC_B32 = auto(); S_NOR_SAVEEXEC_B64 = auto()
    S_XNOR_SAVEEXEC_B32 = auto(); S_XNOR_SAVEEXEC_B64 = auto()
    S_AND_NOT0_SAVEEXEC_B32 = auto(); S_AND_NOT0_SAVEEXEC_B64 = auto()
    S_OR_NOT0_SAVEEXEC_B32 = auto(); S_OR_NOT0_SAVEEXEC_B64 = auto()
    S_AND_NOT1_SAVEEXEC_B32 = auto(); S_AND_NOT1_SAVEEXEC_B64 = auto()
    S_OR_NOT1_SAVEEXEC_B32 = auto(); S_OR_NOT1_SAVEEXEC_B64 = auto()
    S_AND_NOT0_WREXEC_B32 = auto(); S_AND_NOT0_WREXEC_B64 = auto()
    S_AND_NOT1_WREXEC_B32 = auto(); S_AND_NOT1_WREXEC_B64 = auto()
    S_MOVERELS_B32 = auto(); S_MOVERELS_B64 = auto(); S_MOVERELD_B32 = auto()
    S_MOVERELD_B64 = auto(); S_MOVERELSD_2_B32 = auto(); S_GETPC_B64 = auto()
    S_SETPC_B64 = auto(); S_GETPC_B64 = auto(); S_SETPC_B64 = auto()
    S_SWAPPC_B64 = auto(); S_RFE_B64 = auto(); S_RPE_B64 = auto()
    S_SENDMSG_RTN_B32 = auto(); S_SENDMSG_RTN_B64 = auto()


    # ** SOPP - SIMM16 **
    

