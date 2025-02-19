addi sp,zero,256
addi ra,zero,15
addi sp,zero,10
loop: beq ra,sp,end
sub ra,ra,sp
jal zero,loop
end: sw ra,0(sp)
jalr zero,ra,0
beq zero,zero,0
