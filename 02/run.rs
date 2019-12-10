use std::fs::File;
use std::io::prelude::*;

fn run(opcodes: &mut std::vec::Vec<i32>) {
    let mut ip: usize = 0;

    while opcodes[ip] != 99 {
      match opcodes[ip] {
        1 => {
            let op1 = opcodes[opcodes[ip+1] as usize];
            let op2 = opcodes[opcodes[ip+2] as usize];
            let op3 = opcodes[ip+3] as usize;
            opcodes[op3] = op1 + op2;
        }
        2 => {
            let op1 = opcodes[opcodes[ip+1] as usize];
            let op2 = opcodes[opcodes[ip+2] as usize];
            let op3 = opcodes[ip+3] as usize;
            opcodes[op3] = op1 * op2;
        }
        _ => {
          panic!("Unknown opcode");
        }
      } // match
      ip = ip + 4;
    }
}

fn init(opcodes: &Vec<i32>, noun:i32, verb: i32) -> Vec<i32> {
  let mut v = opcodes.clone();
  v[1] = noun;
  v[2] = verb;
  return v;
}

fn main() -> std::io::Result<()>{
    let mut f = File::open("input.txt")?;
    let mut contents = String::new();
    f.read_to_string(&mut contents)?;
    //contents = "1,1,1,4,99,5,6,0,99".to_string();
    let mut v: Vec<i32> = Vec::new();
    for s in contents.trim().split(",") {
      v.push(s.parse::<i32>().unwrap());
    }

    let mut opcodes = init(&v, 12, 2);
    run(&mut opcodes);
  println!("Hello World! {}", opcodes[0]);
  let target:i32 = 19690720;

  for noun in 1..100 {
    for verb in 1..100 {
      let mut opcodes = init(&v, noun, verb);
          run(&mut opcodes);
      if opcodes[0] == target {
        println!("{} {}", noun, verb);
        return Ok(());
      }
    }
  }


  Ok(())
}
