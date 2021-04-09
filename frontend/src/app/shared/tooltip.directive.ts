import { Directive, ElementRef, HostListener, Input, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appTooltip]'
})
export class TooltipDirective {

  tooltip!: HTMLElement;
  @Input() appTooltip: string | undefined = '';
  delay = 500;
  constructor(private el: ElementRef, private renderer: Renderer2) {}
  
  @HostListener("mouseover") onMouseEnter() {
    if (!this.appTooltip){
      return
    }
    this.showTooltip();
  }

  @HostListener("mouseleave") onMouseLeave() {
    this.renderer.removeClass(this.tooltip, "tooltip_show");
     // on mouse over it will remove the opacity
  }

  showTooltip() {
    this.tooltip = this.renderer.createElement("span"); 
    // creating a span
    this.tooltip.appendChild(this.renderer.createElement("span")); 
    // appending a span to the tooltip

    this.renderer.appendChild(
      this.tooltip,
      this.renderer.createText(this.appTooltip ? this.appTooltip : '') 
      // adding the tooltip text into the tooltip span
    );
    const hostPos = this.el.nativeElement.getBoundingClientRect(); 
    // getting the hight width and positions of the target element
    let top, left;

    top = hostPos.bottom;
    left = hostPos.left + hostPos.width / 2;
    this.renderer.setStyle(this.tooltip, "top", `${top}px`); 
    //adding a top positions value for the tooltip
    this.renderer.setStyle(this.tooltip, "left", `${left}px`); 
    // adding the left value
    this.renderer.appendChild(document.body, this.tooltip); 
   // appending to the document
    this.renderer.addClass(this.tooltip, "tooltip"); 
   // adding the tooltip styles
  }

}
