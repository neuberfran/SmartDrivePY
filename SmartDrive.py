#!/usr/bin/env python
#
# Copyright (c) 2014 OpenElectrons.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# History:
# Date      Author      Comments
# 02/03/14  Michael     Initial authoring.
# 04/21/14  Michael     SmartDrive modification
#

## @package SmartDrive
# This is the i2c module for OpenElectrons SmartDrive motor controller.

from OpenElectrons_i2c import OpenElectrons_i2c
import time

## SmartDrive: this class provides motor control functions
class SmartDrive(OpenElectrons_i2c):
    
    SmartDrive_ADDRESS = (0x36)
    SmartDrive_VOLTAGE_MULTIPLIER = 212.7
    
    # Motor selection related constants
    SmartDrive_Motor_1        =        0x01
    SmartDrive_Motor_2        =        0x02
    SmartDrive_Motor_Both     =        0x03

    # Motor action constants
    # stop and let the motor coast.
    SmartDrive_Next_Action_Float   =   0x00
    # apply brakes, and resist change to tachometer
    SmartDrive_Next_Action_Brake   =   0x01
    # apply brakes, and restore externally forced change to tachometer
    SmartDrive_Next_Action_BrakeHold = 0x02
    
    #Direction related constants
    SmartDrive_Direction_Forward   =   0x01
    SmartDrive_Direction_Reverse   =   0x00

    # Tachometer related constants
    SmartDrive_Move_Relative = 0x01
    SmartDrive_Move_Absolute = 0x00

    # Next action (upon completion of current action)
    SmartDrive_Completion_Wait_For   =  0x01
    SmartDrive_Completion_Dont_Wait  = 0x00

    # Commonly used speed constants, these are just convenience constants,
    # You can use any value between 0 and 100.
    SmartDrive_Speed_Full = 90
    SmartDrive_Speed_Medium = 60
    SmartDrive_Speed_Slow  = 25

    SmartDrive_CONTROL_SPEED  =    0x01
    SmartDrive_CONTROL_RAMP   =    0x02
    SmartDrive_CONTROL_RELATIVE =  0x04
    SmartDrive_CONTROL_TACHO  =    0x08
    SmartDrive_CONTROL_BRK    =    0x10
    SmartDrive_CONTROL_ON     =    0x20
    SmartDrive_CONTROL_TIME  =     0x40
    SmartDrive_CONTROL_GO   =      0x80
    
    SmartDrive_COMMAND  =  0x41
    SmartDrive_SETPT_M1  =   0x42
    SmartDrive_SPEED_M1  =   0x46
    SmartDrive_TIME_M1  =    0x47
    SmartDrive_CMD_B_M1  =   0x48
    SmartDrive_CMD_A_M1  =   0x49

    SmartDrive_SETPT_M2  =   0x4A
    SmartDrive_SPEED_M2  =   0x4E
    SmartDrive_TIME_M2   =   0x4F
    SmartDrive_CMD_B_M2  =   0x50
    SmartDrive_CMD_A_M2  =   0x51

    #Read registers.
    SmartDrive_POSITION_M1 = 0x52
    SmartDrive_POSITION_M2 = 0x56
    SmartDrive_STATUS_M1   = 0x5A
    SmartDrive_STATUS_M2   = 0x5B
    SmartDrive_TASKS_M1    = 0x5C
    SmartDrive_TASKS_M2   =  0x5D
    
    #PID control registers
    SmartDrive_P_Kp  =  0x5E            #proportional gain-position
    SmartDrive_P_Ki  =  0x60            #integral gain-position
    SmartDrive_P_Kd  =  0x62            #derivative gain-position
    SmartDrive_S_Kp  =  0x64            #proportional gain-speed
    SmartDrive_S_Ki  =  0x66            #integral gain-speed
    SmartDrive_S_Kd  =  0x68            #derivative gain-speed    
    SmartDrive_PASSCOUNT  =  0x6A
    SmartDrive_PASSTOLERANCE  =  0x6B
    
    SmartDrive_CHKSUM  =  0x6C
    
    #Power data registers
    SmartDrive_BATT_VOLTAGE  =  0x6E
    SmartDrive_RESETSTATUS  =  0x6F
    SmartDrive_CURRENT_M1  =  0x70
    SmartDrive_CURRENT_M2  =  0x72
    
    #Supported I2C commands
    R = 0x52
    S = 0x53
    a = 0x61
    b = 0x62
    c = 0x63
    A = 0x41
    B = 0x42
    C = 0x43
    
    
    ## Initialize the class with the i2c address of your SmartDrive
    #  @param self The object pointer.
    #  @param SmartDrive_address Address of your SmartDrive.
    def __init__(self, SmartDrive_address = SmartDrive_ADDRESS):
        #the SmartDrive address
        OpenElectrons_i2c.__init__(self, SmartDrive_address >> 1)       
      
    ## Writes a specified command on the command register of the SmartDrive
    #  @param self The object pointer.
    #  @param cmd The command you wish the SmartDrive to execute.
    def command(self, cmd):
        print  cmd
        self.writeByte(self.SmartDrive_COMMAND, cmd)       
    
    ## Reads the battery voltage. Multiplier constant not yet verified
    #  @param self The object pointer.
    def GetBattVoltage(self):
        try:
            return self.readByte(self.SmartDrive_BATT_VOLTAGE) * self.SmartDrive_VOLTAGE_MULTIPLIER
        except:
            print "Error: Could not read voltage"
            return ""
            
### Function not supported. May support function in the future.        
#    def GetMotorCurrent(self, motor_number):
#        try:
#             if motor_number == 1:
#                return self.readInteger(self.SmartDrive_CURRENT_M1)
#            if motor_number == 2:
#                return self.readInteger(self.SmartDrive_CURRENT_M2)
#        except:
#            print "Error: Could not read current"
#            return ""
        
    ## Reads the tacheometer position of the specified motor
    #  @param self The object pointer.
    #  @param motor_number Number of the motor you wish to read.
    def ReadTachometerPosition(self, motor_number):
        try:
            if motor_number == 1 :
                return self.readLongSigned(self.SmartDrive_POSITION_M1) 
            if motor_number == 2 :
                return self.readLongSigned(self.SmartDrive_POSITION_M2)
        except:
            print "Error: Could not read encoders"
            return ""
    
    ## Turns the specified motor(s) forever
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) you wish to turn.
    #  @param direction The direction you wish to turn the motor(s).
    #  @param speed The speed at which you wish to turn the motor(s).
    def SmartDrive_Run_Unlimited( self, motor_number, direction, speed):

        ctrl = 0
        ctrl |= self.SmartDrive_CONTROL_SPEED
        ctrl |= self.SmartDrive_CONTROL_BRK
        #print speed
        speed = int(speed)
        
        if ( motor_number != self.SmartDrive_Motor_Both ):
            ctrl |= self.SmartDrive_CONTROL_GO
        if ( direction == self.SmartDrive_Direction_Forward ):
            speed = speed
        if ( direction != self.SmartDrive_Direction_Forward ):
            speed = speed * -1
        if ( (motor_number & 0x01) != 0 ): 
            array = [speed, 0, 0, ctrl]
            self.writeArray( self.SmartDrive_SPEED_M1, array)
        if ( (motor_number & 0x02) != 0 ):
            array = [speed, 0, 0, ctrl]
            self.writeArray( self.SmartDrive_SPEED_M2, array); 
        if ( motor_number == self.SmartDrive_Motor_Both ) :
            self.writeByte(self.SmartDrive_COMMAND, self.S)  

    ## Stops the specified motor(s)
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) you wish to turn.
    #  @param next_action How you wish to stop the motor(s).
    def SmartDrive_Stop( self, motor_number, next_action ):
        
        if ( next_action == self.SmartDrive_Next_Action_Brake or next_action == self.SmartDrive_Next_Action_BrakeHold ):
            if (motor_number == self.SmartDrive_Motor_1):
                self.writeByte(self.SmartDrive_COMMAND, self.A)
            if (motor_number == self.SmartDrive_Motor_2):
                self.writeByte(self.SmartDrive_COMMAND, self.B)
            if (motor_number == self.SmartDrive_Motor_Both):
                self.writeByte(self.SmartDrive_COMMAND, self.C)
        else:
            if (motor_number == self.SmartDrive_Motor_1):
                self.writeByte(self.SmartDrive_COMMAND, self.a)
            if (motor_number == self.SmartDrive_Motor_2):
                self.writeByte(self.SmartDrive_COMMAND, self.b)
            if (motor_number == self.SmartDrive_Motor_Both):
                self.writeByte(self.SmartDrive_COMMAND, self.c)
            
    ## Turns the specified motor(s) for a given amount of seconds
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) you wish to turn.
    #  @param direction The direction you wish to turn the motor(s).
    #  @param speed The speed at which you wish to turn the motor(s).
    #  @param duration The time in seconds you wish to turn the motor(s).
    #  @param wait_for_completion Tells the program when to handle the next line of code.
    #  @param next_action How you wish to stop the motor(s).
    def SmartDrive_Run_Seconds( self, motor_number, direction, speed, duration, wait_for_completion, next_action ):
        
        ctrl = 0
        ctrl |= self.SmartDrive_CONTROL_SPEED
        ctrl |= self.SmartDrive_CONTROL_TIME

        if ( next_action == self.SmartDrive_Next_Action_Brake ):
            ctrl |= self.SmartDrive_CONTROL_BRK
        if ( next_action == self.SmartDrive_Next_Action_BrakeHold ):
            ctrl |= self.SmartDrive_CONTROL_BRK
            ctrl |= self.SmartDrive_CONTROL_ON
        if ( motor_number != self.SmartDrive_Motor_Both ):
            ctrl |= self.SmartDrive_CONTROL_GO
        if ( direction == self.SmartDrive_Direction_Forward ):
            speed = speed
        if ( direction != self.SmartDrive_Direction_Forward ):
            speed = speed * -1    
        if ( (motor_number & 0x01) != 0 ):
            array = [speed, duration, 0, ctrl]
            self.writeArray( self.SmartDrive_SPEED_M1, array) 
        if ( (motor_number & 0x02) != 0 ) :
            array = [speed, duration, 0, ctrl]
            self.writeArray( self.SmartDrive_SPEED_M2, array)
        if ( motor_number == self.SmartDrive_Motor_Both ) :
            self.writeByte(self.SmartDrive_COMMAND, self.S)        
        if ( wait_for_completion == self.SmartDrive_Completion_Wait_For ):
            time.sleep(0.050);  # this delay is required for the status byte to be available for reading.
            self.SmartDrive_WaitUntilTimeDone(motor_number)
            
    ## Waits until the specified time for the motor(s) to run is completed
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) to wait for.
    def SmartDrive_WaitUntilTimeDone(self, motor_number):
        while self.SmartDrive_IsTimeDone(motor_number) != True:
            time.sleep(0.050)        
    
    ## Checks to ensure the specified time for the motor(s) to run is completed.
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) to check.    
    def SmartDrive_IsTimeDone(self, motor_number):
        if ( motor_number == self.SmartDrive_Motor_1 ):
            result = self.readByte(self.SmartDrive_STATUS_M1)
            # look for the time bit to be zero.
            if (( result & 0x40 ) == 0 ):
                return True         
        elif ( motor_number == self.SmartDrive_Motor_2 ) :
            result = self.readByte(self.SmartDrive_STATUS_M2)
            # look for the time bit to be zero.
            if (( result & 0x40 ) == 0 ):
                return True
        elif ( motor_number == self.SmartDrive_Motor_Both ):
            result = self.readByte(self.SmartDrive_STATUS_M1)
            result2 = self.readByte(self.SmartDrive_STATUS_M2)
            # look for both time bits to be zero
            if (((result & 0x40) == 0) &((result2 & 0x40) == 0) ):
                return True
        else :
            return False
            
    ## Turns the specified motor(s) for given relative tacheometer count
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) you wish to turn.
    #  @param direction The direction you wish to turn the motor(s).
    #  @param speed The speed at which you wish to turn the motor(s).
    #  @param degrees The relative tacheometer count you wish to turn the motor(s).
    #  @param wait_for_completion Tells the program when to handle the next line of code.
    #  @param next_action How you wish to stop the motor(s).
    def SmartDrive_Run_Degrees(self, motor_number, direction, speed, degrees, wait_for_completion, next_action):
        
        ctrl = 0
        ctrl |= self.SmartDrive_CONTROL_SPEED
        ctrl |= self.SmartDrive_CONTROL_TACHO
        ctrl |= self.SmartDrive_CONTROL_RELATIVE
        
        if ( direction == self.SmartDrive_Direction_Forward ):
            d = degrees
        if ( direction != self.SmartDrive_Direction_Forward ):
            d = degrees * -1 
        
        t4 = (d/0x1000000)
        t3 = ((d%0x1000000)/0x10000)
        t2 = (((d%0x1000000)%0x10000)/0x100)
        t1 = (((d%0x1000000)%0x10000)%0x100)
        
        if ( next_action == self.SmartDrive_Next_Action_Brake ):
            ctrl |= self.SmartDrive_CONTROL_BRK
        if ( next_action == self.SmartDrive_Next_Action_BrakeHold ):
            ctrl |= self.SmartDrive_CONTROL_BRK
            ctrl |= self.SmartDrive_CONTROL_ON
        if ( motor_number != self.SmartDrive_Motor_Both ):
            ctrl |= self.SmartDrive_CONTROL_GO        
        if ( (motor_number & 0x01) != 0 ):
            array = [t1, t2, t3, t4, speed, 0, 0, ctrl]
            self.writeArray(self.SmartDrive_SETPT_M1, array) 
        if ( (motor_number & 0x02) != 0 ) :
            array = [t1, t2, t3, t4, speed, 0, 0, ctrl]
            self.writeArray(self.SmartDrive_SETPT_M2, array) 
        if ( motor_number == self.SmartDrive_Motor_Both ) :
            self.writeByte(self.SmartDrive_COMMAND, self.S)         
        if ( wait_for_completion == self.SmartDrive_Completion_Wait_For ):
            time.sleep(0.050);  # this delay is required for the status byte to be available for reading.
            self.SmartDrive_WaitUntilTachoDone(motor_number)
            
    ## Turns the specified motor(s) for given relative tacheometer count
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) you wish to turn.
    #  @param direction The direction you wish to turn the motor(s).
    #  @param speed The speed at which you wish to turn the motor(s).
    #  @param rotations The relative amount of rotations you wish to turn the motor(s).
    #  @param wait_for_completion Tells the program when to handle the next line of code.
    #  @param next_action How you wish to stop the motor(s).
    def SmartDrive_Run_Rotations(self, motor_number, direction, speed, rotations, wait_for_completion, next_action):
        
        ctrl = 0
        ctrl |= self.SmartDrive_CONTROL_SPEED
        ctrl |= self.SmartDrive_CONTROL_TACHO
        ctrl |= self.SmartDrive_CONTROL_RELATIVE
        
        if ( direction == self.SmartDrive_Direction_Forward ):
            d = rotations * 360
        if ( direction != self.SmartDrive_Direction_Forward ):
            d = (rotations * 360) * -1 
        
        t4 = (d/0x1000000)
        t3 = ((d%0x1000000)/0x10000)
        t2 = (((d%0x1000000)%0x10000)/0x100)
        t1 = (((d%0x1000000)%0x10000)%0x100)
        
        if ( next_action == self.SmartDrive_Next_Action_Brake ):
            ctrl |= self.SmartDrive_CONTROL_BRK
        if ( next_action == self.SmartDrive_Next_Action_BrakeHold ):
            ctrl |= self.SmartDrive_CONTROL_BRK
            ctrl |= self.SmartDrive_CONTROL_ON
        if ( motor_number != self.SmartDrive_Motor_Both ):
            ctrl |= self.SmartDrive_CONTROL_GO
        if ( (motor_number & 0x01) != 0 ):
            array = [t1, t2, t3, t4, speed, 0, 0, ctrl]
            self.writeArray(self.SmartDrive_SETPT_M1, array) 
        if ( (motor_number & 0x02) != 0 ) :
            array = [t1, t2, t3, t4, speed, 0, 0, ctrl]
            self.writeArray(self.SmartDrive_SETPT_M2, array) 
        if ( motor_number == self.SmartDrive_Motor_Both ) :
            self.writeByte(self.SmartDrive_COMMAND, self.S)        
        if ( wait_for_completion == self.SmartDrive_Completion_Wait_For ):
            time.sleep(0.050);  # this delay is required for the status byte to be available for reading.
            self.SmartDrive_WaitUntilTachoDone(motor_number)
    
    ## Turns the specified motor(s) for given absolute tacheometer count
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) you wish to turn.
    #  @param direction The direction you wish to turn the motor(s).
    #  @param speed The speed at which you wish to turn the motor(s).
    #  @param tacho_count The absolute tacheometer count you wish to turn the motor(s).
    #  @param wait_for_completion Tells the program when to handle the next line of code.
    #  @param next_action How you wish to stop the motor(s).
    def SmartDrive_Run_Tacho(self, motor_number, speed, tacho_count, wait_for_completion, next_action):
        
        ctrl = 0
        ctrl |= self.SmartDrive_CONTROL_SPEED
        ctrl |= self.SmartDrive_CONTROL_TACHO
        d = tacho_count
        
        t4 = (d/0x1000000)
        t3 = ((d%0x1000000)/0x10000)
        t2 = (((d%0x1000000)%0x10000)/0x100)
        t1 = (((d%0x1000000)%0x10000)%0x100)
        
        if ( next_action == self.SmartDrive_Next_Action_Brake ):
            ctrl |= self.SmartDrive_CONTROL_BRK
        if ( next_action == self.SmartDrive_Next_Action_BrakeHold ):
            ctrl |= self.SmartDrive_CONTROL_BRK
            ctrl |= self.SmartDrive_CONTROL_ON
        if ( motor_number != self.SmartDrive_Motor_Both ):
            ctrl |= self.SmartDrive_CONTROL_GO
        if ( (motor_number & 0x01) != 0 ):
            array = [t1, t2, t3, t4, speed, 0, 0, ctrl]
            self.writeArray(self.SmartDrive_SETPT_M1, array) 
        if ( (motor_number & 0x02) != 0 ) :
            array = [t1, t2, t3, t4, speed, 0, 0, ctrl]
            self.writeArray(self.SmartDrive_SETPT_M2, array) 
        if ( motor_number == self.SmartDrive_Motor_Both ) :
            self.writeByte(self.SmartDrive_COMMAND, self.S)         
        if ( wait_for_completion == self.SmartDrive_Completion_Wait_For ):
            time.sleep(0.050);  # this delay is required for the status byte to be available for reading.
            self.SmartDrive_WaitUntilTachoDone(motor_number) 
    
    ## Waits until the specified tacheomter count for the motor(s) to run is reached.
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) to wait for.
    def SmartDrive_WaitUntilTachoDone(self, motor_number):
        while self.SmartDrive_IsTachoDone(motor_number) != True:
            time.sleep(0.050)        
        
    ## Checks to ensure the specified tacheomter count for the motor(s) to run is reached.
    #  @param self The object pointer.
    #  @param motor_number Number of the motor(s) to check. 
    def SmartDrive_IsTachoDone(self, motor_number):
        if ( motor_number == self.SmartDrive_Motor_1 ):
            result = self.readByte(self.SmartDrive_STATUS_M1)
            # look for the time bit to be zero.
            if (( result & 0x08 ) == 0 ):
                return True         
        elif ( motor_number == self.SmartDrive_Motor_2 ) :
            result = self.readByte(self.SmartDrive_STATUS_M2)
            # look for the time bit to be zero.
            if (( result & 0x08 ) == 0 ):
                return True
        elif ( motor_number == self.SmartDrive_Motor_Both ):
            result = self.readByte(self.SmartDrive_STATUS_M1)
            result2 = self.readByte(self.SmartDrive_STATUS_M2)
            # look for both time bits to be zero
            if (((result & 0x08) == 0) & ((result2 & 0x08) == 0) ):
                return True
        else :
            return False

    ## Writes user specified values to the PID control registers
    #  @param self The object pointer.
    #  @param Kp_tacho Proportional-gain of the tacheometer position of the motor.
    #  @param Ki_tacho Integral-gain of the tacheometer position of the motor.
    #  @param Kd_tacho Derivative-gain of the tacheometer position of the motor.
    #  @param Kp_speed Proportional-gain of the speed of the motor.
    #  @param Ki_speed Integral-gain of the speed of the motor.
    #  @param Kd_speed Derivative-gain of the speed of the motor.
    def SetPerformanceParameters(self, Kp_tacho, Ki_tacho, Kd_tacho, Kp_speed, Ki_speed, Kd_speed, passcount, tolerance):
        
        Kp_t1 = Kp_tacho%0x100
        Kp_t2 = Kp_tacho/0x100      
        Ki_t1 = Ki_tacho%0x100
        Ki_t2 = Ki_tacho/0x100
        Kd_t1 = Kd_tacho%0x100
        Kd_t2 = Kd_tacho/0x100
        Kp_s1 = Kp_speed%0x100        
        Kp_s2 = Kp_speed/0x100
        Ki_s1 = Ki_speed%0x100 
        Ki_s2 = Ki_speed/0x100
        Kd_s1 = Kd_speed%0x100
        Kd_s2 = Kd_speed/0x100
        passcount = passcount
        tolerance = tolerance
        array = [Kp_t1 , Kp_t2 , Ki_t1, Ki_t2, Kd_t1, Kd_t2, Kp_s1, Kp_s2, Ki_s1, Ki_s2, Kd_s1, Kd_s2, passcount, tolerance]
        self.writeArray(self.SmartDrive_P_Kp, array)
        
    ## Reads the values of the PID control registers
    #  @param self The object pointer.
    def ReadPerformanceParameters(self):
    
        try:
            print "Pkp: " + str(self.readInteger(self.SmartDrive_P_Kp))
            print "Pki: " + str(self.readInteger(self.SmartDrive_P_Ki))
            print "Pkd: " + str(self.readInteger(self.SmartDrive_P_Kd))
            print "Skp: " + str(self.readInteger(self.SmartDrive_S_Kp))
            print "Ski: " + str(self.readInteger(self.SmartDrive_S_Ki))
            print "Skd: " + str(self.readInteger(self.SmartDrive_S_Kd))
            print "Passcount: " + str(self.SmartDrive_PASSCOUNT)
            print "Tolerance: " + str(self.SmartDrive_PASSTOLERANCE)
        except:
            print "Error: Could not read PID values"
            return ""