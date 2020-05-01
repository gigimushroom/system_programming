	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 10, 15	sdk_version 10, 15
	.globl	_bt                     ## -- Begin function bt
	.p2align	4, 0x90
_bt:                                    ## @bt
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$848, %rsp              ## imm = 0x350
	leaq	-816(%rbp), %rdi
	movq	___stack_chk_guard@GOTPCREL(%rip), %rax
	movq	(%rax), %rax
	movq	%rax, -8(%rbp)
	movl	$100, %esi
	callq	_backtrace
	movl	%eax, -824(%rbp)
	movl	-824(%rbp), %esi
	leaq	L_.str(%rip), %rdi
	movb	$0, %al
	callq	_printf
	leaq	-816(%rbp), %rdi
	movl	-824(%rbp), %esi
	movl	%eax, -836(%rbp)        ## 4-byte Spill
	callq	_backtrace_symbols
	movq	%rax, -832(%rbp)
	movl	$0, -820(%rbp)
LBB0_1:                                 ## =>This Inner Loop Header: Depth=1
	movl	-820(%rbp), %eax
	cmpl	-824(%rbp), %eax
	jge	LBB0_4
## %bb.2:                               ##   in Loop: Header=BB0_1 Depth=1
	movq	-832(%rbp), %rax
	movslq	-820(%rbp), %rcx
	movq	(%rax,%rcx,8), %rsi
	leaq	L_.str.1(%rip), %rdi
	movb	$0, %al
	callq	_printf
	movl	%eax, -840(%rbp)        ## 4-byte Spill
## %bb.3:                               ##   in Loop: Header=BB0_1 Depth=1
	movl	-820(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -820(%rbp)
	jmp	LBB0_1
LBB0_4:
	movq	___stack_chk_guard@GOTPCREL(%rip), %rax
	movq	(%rax), %rax
	movq	-8(%rbp), %rcx
	cmpq	%rcx, %rax
	jne	LBB0_6
## %bb.5:
	addq	$848, %rsp              ## imm = 0x350
	popq	%rbp
	retq
LBB0_6:
	callq	___stack_chk_fail
	ud2
	.cfi_endproc
                                        ## -- End function
	.globl	_list_init              ## -- Begin function list_init
	.p2align	4, 0x90
_list_init:                             ## @list_init
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_list_insert            ## -- Begin function list_insert
	.p2align	4, 0x90
_list_insert:                           ## @list_insert
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	$8, %edi
	callq	_malloc
	movq	_l@GOTPCREL(%rip), %rdi
	movq	%rax, -16(%rbp)
	movl	-4(%rbp), %ecx
	movq	-16(%rbp), %rax
	movl	%ecx, (%rax)
	cmpq	$0, (%rdi)
	jne	LBB2_2
## %bb.1:
	movq	_l@GOTPCREL(%rip), %rax
	movq	-16(%rbp), %rcx
	movq	%rcx, (%rax)
	jmp	LBB2_3
LBB2_2:
	movq	_l@GOTPCREL(%rip), %rax
	movq	(%rax), %rcx
	movq	-16(%rbp), %rdx
	movq	%rcx, 8(%rdx)
	movq	-16(%rbp), %rcx
	movq	%rcx, (%rax)
LBB2_3:
	addq	$16, %rsp
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_list_search            ## -- Begin function list_search
	.p2align	4, 0x90
_list_search:                           ## @list_search
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	movq	_l@GOTPCREL(%rip), %rax
	movl	%edi, -8(%rbp)
	movq	(%rax), %rax
	movq	%rax, -16(%rbp)
LBB3_1:                                 ## =>This Inner Loop Header: Depth=1
	cmpq	$0, -16(%rbp)
	je	LBB3_5
## %bb.2:                               ##   in Loop: Header=BB3_1 Depth=1
	movq	-16(%rbp), %rax
	movl	(%rax), %ecx
	cmpl	-8(%rbp), %ecx
	jne	LBB3_4
## %bb.3:
	movl	$1, -4(%rbp)
	jmp	LBB3_6
LBB3_4:                                 ##   in Loop: Header=BB3_1 Depth=1
	movq	-16(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -16(%rbp)
	jmp	LBB3_1
LBB3_5:
	movl	$0, -4(%rbp)
LBB3_6:
	movl	-4(%rbp), %eax
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_list_delete            ## -- Begin function list_delete
	.p2align	4, 0x90
_list_delete:                           ## @list_delete
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	movq	_l@GOTPCREL(%rip), %rax
	movl	%edi, -8(%rbp)
	cmpq	$0, (%rax)
	jne	LBB4_2
## %bb.1:
	movl	$0, -4(%rbp)
	jmp	LBB4_12
LBB4_2:
	movq	_l@GOTPCREL(%rip), %rax
	movq	(%rax), %rax
	movl	(%rax), %ecx
	cmpl	-8(%rbp), %ecx
	jne	LBB4_4
## %bb.3:
	movq	_l@GOTPCREL(%rip), %rax
	movq	(%rax), %rcx
	movq	8(%rcx), %rcx
	movq	%rcx, (%rax)
	movl	$1, -4(%rbp)
	jmp	LBB4_12
LBB4_4:
	movq	_l@GOTPCREL(%rip), %rax
	movq	(%rax), %rax
	movq	%rax, -16(%rbp)
LBB4_5:                                 ## =>This Inner Loop Header: Depth=1
	xorl	%eax, %eax
	movb	%al, %cl
	cmpq	$0, -16(%rbp)
	movb	%cl, -17(%rbp)          ## 1-byte Spill
	je	LBB4_7
## %bb.6:                               ##   in Loop: Header=BB4_5 Depth=1
	movq	-16(%rbp), %rax
	cmpq	$0, 8(%rax)
	setne	%cl
	movb	%cl, -17(%rbp)          ## 1-byte Spill
LBB4_7:                                 ##   in Loop: Header=BB4_5 Depth=1
	movb	-17(%rbp), %al          ## 1-byte Reload
	testb	$1, %al
	jne	LBB4_8
	jmp	LBB4_11
LBB4_8:                                 ##   in Loop: Header=BB4_5 Depth=1
	movq	-16(%rbp), %rax
	movq	8(%rax), %rax
	movl	(%rax), %ecx
	cmpl	-8(%rbp), %ecx
	jne	LBB4_10
## %bb.9:
	movq	-16(%rbp), %rax
	movq	8(%rax), %rax
	movq	8(%rax), %rax
	movq	-16(%rbp), %rcx
	movq	%rax, 8(%rcx)
	movl	$1, -4(%rbp)
	jmp	LBB4_12
LBB4_10:                                ##   in Loop: Header=BB4_5 Depth=1
	movq	-16(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -16(%rbp)
	jmp	LBB4_5
LBB4_11:
	movl	$0, -4(%rbp)
LBB4_12:
	movl	-4(%rbp), %eax
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_list_dump              ## -- Begin function list_dump
	.p2align	4, 0x90
_list_dump:                             ## @list_dump
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	_l@GOTPCREL(%rip), %rax
	movq	(%rax), %rax
	movq	%rax, -8(%rbp)
	leaq	L_.str.2(%rip), %rdi
	movb	$0, %al
	callq	_printf
	movl	%eax, -12(%rbp)         ## 4-byte Spill
LBB5_1:                                 ## =>This Inner Loop Header: Depth=1
	cmpq	$0, -8(%rbp)
	je	LBB5_3
## %bb.2:                               ##   in Loop: Header=BB5_1 Depth=1
	movq	-8(%rbp), %rax
	movl	(%rax), %esi
	leaq	L_.str.3(%rip), %rdi
	movb	$0, %al
	callq	_printf
	movq	-8(%rbp), %rdi
	movq	8(%rdi), %rdi
	movq	%rdi, -8(%rbp)
	movl	%eax, -16(%rbp)         ## 4-byte Spill
	jmp	LBB5_1
LBB5_3:
	leaq	L_.str.4(%rip), %rdi
	movb	$0, %al
	callq	_printf
	movl	%eax, -20(%rbp)         ## 4-byte Spill
	addq	$32, %rsp
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_list_size              ## -- Begin function list_size
	.p2align	4, 0x90
_list_size:                             ## @list_size
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	movq	_l@GOTPCREL(%rip), %rax
	movl	$0, -4(%rbp)
	movq	(%rax), %rax
	movq	%rax, -16(%rbp)
LBB6_1:                                 ## =>This Inner Loop Header: Depth=1
	cmpq	$0, -16(%rbp)
	je	LBB6_3
## %bb.2:                               ##   in Loop: Header=BB6_1 Depth=1
	movl	-4(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -4(%rbp)
	movq	-16(%rbp), %rcx
	movq	8(%rcx), %rcx
	movq	%rcx, -16(%rbp)
	jmp	LBB6_1
LBB6_3:
	movl	-4(%rbp), %eax
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	__test_help             ## -- Begin function _test_help
	.p2align	4, 0x90
__test_help:                            ## @_test_help
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %esi
	cmpl	-8(%rbp), %esi
	je	LBB7_2
## %bb.1:
	movl	-4(%rbp), %esi
	movl	-8(%rbp), %edx
	leaq	L_.str.5(%rip), %rdi
	movb	$0, %al
	callq	_printf
	movl	%eax, -12(%rbp)         ## 4-byte Spill
	callq	_bt
LBB7_2:
	addq	$16, %rsp
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_main                   ## -- Begin function main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	$0, -4(%rbp)
	movl	$3, %edi
	callq	_list_insert
	movl	$4, %edi
	callq	_list_insert
	movl	$5, %edi
	callq	_list_insert
	callq	_list_size
	movl	%eax, %edi
	movl	$3, %esi
	callq	__test_help
	movl	$3, %edi
	callq	_list_search
	movl	%eax, %edi
	movl	$1, %esi
	callq	__test_help
	movl	$6, %edi
	callq	_list_search
	xorl	%esi, %esi
	movl	%eax, %edi
	callq	__test_help
	movl	$5, %edi
	callq	_list_delete
	movl	%eax, -8(%rbp)          ## 4-byte Spill
	callq	_list_size
	movl	%eax, %edi
	movl	$2, %esi
	callq	__test_help
	movl	$3, %edi
	callq	_list_delete
	movl	$4, %edi
	movl	%eax, -12(%rbp)         ## 4-byte Spill
	callq	_list_delete
	movl	%eax, -16(%rbp)         ## 4-byte Spill
	callq	_list_size
	xorl	%esi, %esi
	movl	%eax, %edi
	callq	__test_help
	callq	_list_size
	movl	%eax, %edi
	movl	$1, %esi
	callq	__test_help
	xorl	%eax, %eax
	addq	$16, %rsp
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"backtrace() returned %d addresses\n"

L_.str.1:                               ## @.str.1
	.asciz	"%s\n"

	.comm	_l,8,3                  ## @l
L_.str.2:                               ## @.str.2
	.asciz	"Dumping list:"

L_.str.3:                               ## @.str.3
	.asciz	" %d"

L_.str.4:                               ## @.str.4
	.asciz	"\n"

L_.str.5:                               ## @.str.5
	.asciz	"ERROR: get %d, expected: %d\n"


.subsections_via_symbols
