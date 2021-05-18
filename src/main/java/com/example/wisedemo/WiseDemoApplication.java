package com.example.wisedemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class WiseDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(WiseDemoApplication.class, args);
    }
    
    @RestController
    static final class MyController{

        @GetMapping("/")
        String hello() {
            return "Hello World222!\n";
        }
    }
}
