/*
   Speedclimbing_timer

   Using an Arduino to accurately measure the time for speedclimbing.
   Outputs the stopped time over serial at a baud rate of 9600 bps.

   Usage:
   - push the button once to start the countdown
   - step on the pad
   - 0.1 seconds after the green signal flashes, start climbing
   - touch the top pad
   - read the serial
   - at any time you can press the button to abort the timing process

   The circut:
   - three signal LEDs attached to the pins at 'red_led', 'yellow_led' and 'green_led'
   - a sending indicator at 'serial_indicator'
   - a button for starting and aborting the timer at pin 'button'
   - two pressure sensing pads at pins 'pad_1' and 'pad_2'

   created 26. Aug 2018
   by Maximilian Lohmann
*/


/* constant variables */
const int IDLING = 0, RED = 1, YELLOW = 2, GREEN = 3, COUNTDOWN_TIMER = 4, WAITING = 5, FALSE_START = 6, BLINK = 7, ABORT = 8, TOPPED = 9, RESET = 10;
const int red_led = 2, yellow_led = 3, green_led = 4, serial_indicator = 5;
const int button = 11, pad_1 = 12, pad_2 = 13, PAD_THRESHHOLD = 512;

/* normal variables */
unsigned int current_state, prev_state, blink_counter;
unsigned long result, timer, delay_start;



/* SIGNAL FUNCTIONS */

// function changing the states of the signals, given a state (0 is off, 1 is on) for each led
void change_signals(int red, int yellow, int green) {
  digitalWrite(red_led, red);
  digitalWrite(yellow_led, yellow);
  digitalWrite(green_led, green);
}

void off() {
  change_signals(0, 0, 0);
}


/* TIMER FUNCTIONS */

// function sets the start of the timer to the current time if passed_state is different from prev_state
void set_timer(int passed_state) {
  if (prev_state != passed_state)
    timer = millis();
}


/* SERIAL FUNCTIONS */

void send_result() {
  // sending...
  digitalWrite(serial_indicator, HIGH);
  Serial.println(result);
  digitalWrite(serial_indicator, LOW);
}


/* TRANSITION FUNCTIONS */

// function setting current state to next_state
void change_state(int next_state) {
  prev_state = current_state;
  current_state = next_state;
}


// function used in the countdown procedure
// checking button for abort, pad1 for falsestart and timer for timer_ending
void countdown_transitions() {
  if (digitalRead(button) == HIGH) change_state(ABORT);
  else if (analogRead(pad_1) == HIGH) change_state(FALSE_START);
  else if (millis() > timer + 1000) change_state(current_state + 1);
  else prev_state = current_state; // if the state stays at the current state, setting the prev_state to current state
}


/* STATE FUNCTIONS */

// state only watches out for state changes
void idling() {
  if (digitalRead(button) == HIGH) {
    change_state(RED);
  }
  else prev_state = current_state;
}

// this state takes the parameter state, which can be either RED, YELLOW or GREEN, and changes the signal accordingly. It also
void set_signal(int state) {
  set_timer(state);
  change_signals(state == RED, state == YELLOW, state == GREEN);
  countdown_transitions();
}


void green() {
  change_signals(0,0,1);
  change_state(COUNTDOWN_TIMER);
}

// as a rule, the contestant made a false start, if he lifts his feet within the time of the signa start until 1/10 seconds after the start signal was given
// this state checks enforces rule
void countdown_timer() {
  // initializing the timer
  set_timer(COUNTDOWN_TIMER);
  // checking for a false start
  if (analogRead(pad_1) > PAD_THRESHHOLD) change_state(FALSE_START);
  else if (digitalRead(button) == HIGH) change_state(ABORT);
  // checking if the 1/10 second is over
  else if (timer + 100 < millis()) change_state(WAITING);
  else prev_state = current_state;
}

// this state waits until pad_2 or button is pressed
void waiting() {
  if (analogRead(pad_2) > PAD_THRESHHOLD) change_state(TOPPED);
  else if (digitalRead(button)) change_state(ABORT);
  else prev_state = current_state;
}

void false_start() {
  result = 0;
  send_result();
  change_state(RESET);
}

void blinking() {
  set_timer(BLINK);
  if (timer + 3000 == millis()) change_state(RESET);
  else if (timer + blink_counter * 500) {
    // switching the red signal on or off based on blink_counter
    change_signals(blink_counter % 2, 0, 0);
    blink_counter++;
  }
  else prev_state = current_state;
}

void aborting() {
  result = 0;
  send_result();
  change_state(RESET);
}

void topped() {
  result = millis() - timer;
  send_result();
  change_state(RESET);
}

void reset() {
  // turning the signal off
  off();
  // reset the result
  result = 0;
  blink_counter = 0;
  change_state(IDLING);
}


void transitions() {
  switch (current_state) {
    case IDLING:
      idling(); break;
    case RED:
      set_signal(RED); break;
    case YELLOW:
      set_signal(YELLOW); break;
    case GREEN:
      green(); break;
    case COUNTDOWN_TIMER:
      countdown_timer(); break;
    case WAITING:
      waiting(); break;
    case FALSE_START:
      false_start(); break;
    case BLINK:
      blinking(); break;
    case ABORT:
      aborting(); break;
    case TOPPED:
      topped(); break;
    case RESET:
      reset(); break;
    default:
      // in case of any abnormal event the state gets reset to the idling state
      change_state(IDLING);
  }
}

void setup() {
  prev_state = 0;
  current_state = 0;
  result = 0;
  blink_counter = 0;
  pinMode(red_led, OUTPUT); pinMode(yellow_led, OUTPUT); pinMode(green_led, OUTPUT); pinMode(serial_indicator, OUTPUT);
  pinMode(button, INPUT); pinMode(pad_1, INPUT); pinMode(pad_2, INPUT);
}

void loop() {
  transitions();
}
