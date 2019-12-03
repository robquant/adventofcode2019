use std::fs::File;
use std::io::{BufRead, BufReader};

fn fuel(weight: i32) -> i32 {
   let mut w = weight;
   let mut sum: i32 = 0;
   while w > 0 {
       w = w/3 - 2;
       if w > 0 {
         sum += w;
       }
   }
   return sum;
}

fn main() {
    let file = File::open("input.txt").unwrap();
    let reader = BufReader::new(file);

    let mut sum1: i32 = 0;
    let mut sum2: i32 = 0;
    for line in reader.lines() {
        let unwr = line.unwrap();
        let weight = match unwr.parse::<i32>() {
             Ok(w) => w,
             Err(_) => break,
        };
        sum1 += weight/3 - 2;
        sum2 += fuel(weight);
    }
    println!("Sum: {:?}", sum1);
    println!("Sum: {:?}", sum2);
}
