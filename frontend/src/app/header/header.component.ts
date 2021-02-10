import { ThrowStmt } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  menuOpened = false;

  constructor() { }

  ngOnInit(): void {
  }

  onOpenMenu(){
    this.menuOpened = true;
  }

  onCloseMenu(){
    this.menuOpened = false;
  }

}
